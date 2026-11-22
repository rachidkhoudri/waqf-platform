"""
اختبارات الوقف المستقل وفترة التراجع (72 ساعة) وسحب المبلغ وفق المادة 19 من القانون 25-06
"""
import sys
import os
import uuid
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_independent_waqf_and_cooling_off_withdraw():
    uid = uuid.uuid4().hex[:6]
    test_phone = f"055{int(uuid.uuid4().int % 9000000 + 1000000)}"
    test_email = f"waqif_{uid}@test.dz"

    # تسجيل وتفعيل
    r_reg = client.post("/api/auth/register", json={
        "full_name": "سليمان الجزائري",
        "phone": test_phone,
        "email": test_email,
        "password": "Password123",
        "accept_terms": True
    })
    token = client.post("/api/auth/verify-otp", json={
        "phone_or_email": test_phone,
        "otp_code": r_reg.json()["mock_otp_for_testing"]
    }).json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    client.post(f"/api/auth/admin/kyc/approve/{r_reg.json()['user_id']}", headers=headers)
    client.post("/api/auth/select-roles", headers=headers, json={"is_waqif": True})

    # إيداع وقف مؤقت محدد بـ 24 شهراً
    r_waqf = client.post("/api/waqf/create", headers=headers, json={
        "waqf_title": "وقف رعاية المساجد المؤقت",
        "amount": 75000.0,
        "payment_method": "EDAHABIA",
        "waqf_type": "TEMPORARY",
        "temporary_months": 24,
        "temporary_destination": "يعاد للواقف بعد انقضاء السنتين",
        "risk_preference": "CONSERVATIVE",
        "conditions": [
            {
                "category_id": "mosques",
                "percentage": 100.0,
                "geographic_scope": "ولاية الجزائر",
                "custom_condition_notes": "صيانة أجهزة التكييف"
            }
        ]
    })
    assert r_waqf.status_code == 200
    fund_id = r_waqf.json()["waqf_fund"]["id"]
    assert r_waqf.json()["waqf_fund"]["status"] == "PENDING_COOLING_OFF"

    # سحب المبلغ خلال فترة التراجع 72 ساعة (إلغاء الوقف)
    r_withdraw = client.post(f"/api/waqf/fund/{fund_id}/withdraw-cooling-off", headers=headers)
    assert r_withdraw.status_code == 200
    assert r_withdraw.json()["success"] is True
    assert r_withdraw.json()["refund_amount"] == 75000.0
    print("[PASS] test_independent_waqf_and_cooling_off_withdraw")

if __name__ == "__main__":
    test_independent_waqf_and_cooling_off_withdraw()

