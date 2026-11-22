"""
اختبار شامل وتكاملي للسيناريو الكامل لمنصة وقف تاك (المراحل من 1 إلى 13)
متوافق مع القانون الجزائري 25-06
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.waqf import WaqfFund
from app.models.project import Project
from app.models.funding import ProjectFunding

client = TestClient(app)

def test_full_scenario_e2e():
    print("\n--- بدء اختبار السيناريو الكامل لمنصة وقف تاك (WaqfTech) ---")

    import uuid
    uid = uuid.uuid4().hex[:6]
    test_email = f"omar_{uid}@test.dz"
    test_phone = f"055{int(uuid.uuid4().int % 9000000 + 1000000)}"

    # 1. المرحلة الأولى: التسجيل وفتح الحساب (الخطوات 1 - 5)
    reg_payload = {
        "full_name": "عمر بن رابح الجزائري",
        "phone": test_phone,
        "email": test_email,
        "password": "Password123456",
        "accept_terms": True
    }
    r = client.post("/api/auth/register", json=reg_payload)
    assert r.status_code == 200, r.text
    reg_data = r.json()
    assert reg_data["success"] is True
    otp = reg_data["mock_otp_for_testing"]
    user_id = reg_data["user_id"]
    print(f"[1] تم التسجيل بنجاح (المستخدم: {user_id})")

    # تأكيد الهاتف برمز OTP (الخطوة 5)
    r_otp = client.post("/api/auth/verify-otp", json={
        "phone_or_email": test_phone,
        "otp_code": otp
    })
    assert r_otp.status_code == 200
    token = r_otp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[2] تم تفعيل الحساب برمز التحقق (OTP)")

    # رفع وثائق KYC (الخطوات 6 - 8)
    r_kyc = client.post("/api/auth/kyc/submit", headers=headers, data={
        "id_type": "بطاقة التعريف البيومترية الوطنية",
        "id_number": "199016123456789",
        "id_doc_mock": "docs/id_omar.jpg",
        "selfie_mock": "docs/selfie_omar.jpg"
    })
    assert r_kyc.status_code == 200
    # اعتماد المشرف
    r_appr = client.post(f"/api/auth/admin/kyc/approve/{user_id}", headers=headers)
    assert r_appr.status_code == 200
    print("[3] تم استكمال التحقق من الهوية (KYC) وتفعيل الحساب")

    # 2. المرحلة الثانية: اختيار نوع الحساب (الخطوات 9 - 11)
    r_role = client.post("/api/auth/select-roles", headers=headers, json={
        "is_waqif": True,
        "is_funder": True,
        "is_project_owner": False,
        "is_beneficiary": False
    })
    assert r_role.status_code == 200
    print("[4] تم اختيار الدور: واقف وممول في آن واحد")

    # 3. المسار الأول: حساب الواقف (المراحل 3 - 5: إيداع وقف وتحديد شرطه والتعاقد)
    waqf_payload = {
        "waqf_title": "وقف رعاية طلبة العلم واليتامى المستقل",
        "amount": 100000.0, # 100 ألف دينار جزائري
        "payment_method": "CIB_CARD",
        "waqf_type": "PERPETUAL",
        "risk_preference": "CONSERVATIVE",
        "conditions": [
            {
                "category_id": "education",
                "percentage": 50.0,
                "geographic_scope": "ولاية الجزائر والبليدة",
                "custom_condition_notes": "منح دراسية للمتفوقين"
            },
            {
                "category_id": "orphans",
                "percentage": 50.0,
                "geographic_scope": "عموم الوطن",
                "custom_condition_notes": "رعاية تعليمية للأيتام"
            }
        ]
    }
    r_waqf = client.post("/api/waqf/create", headers=headers, json=waqf_payload)
    assert r_waqf.status_code == 200, r_waqf.text
    waqf_res = r_waqf.json()["waqf_fund"]
    waqf_id = waqf_res["id"]
    waqf_code = waqf_res["waqf_code"]
    print(f"[5] تم إنشاء الوقف المستقل برمز ({waqf_code}) ومبلغ {waqf_res['capital_corpus']:,.2f} د.ج مع فترة 72 ساعة تراجع")

    # المرحلة 5: قراءة عقد الوقف الإلكتروني
    r_ctr = client.get(f"/api/waqf/fund/{waqf_id}/contract", headers=headers)
    assert r_ctr.status_code == 200
    assert "القانون رقم 25-06" in r_ctr.json()["contract_text"]
    assert "أجرة ناظر" in r_ctr.json()["contract_text"]
    print("[6] تم استخراج عقد الوقف الإلكتروني الموثق وفق القانون 25-06 بنجاح")

    # المرحلة 6: استخراج شهادة الوقف الرقمية
    r_cert = client.get(f"/api/waqf/fund/{waqf_id}/certificate", headers=headers)
    assert r_cert.status_code == 200
    assert r_cert.json()["waqf_code"] == waqf_code
    print("[7] تم استخراج شهادة الوقف الرقمية الرسمية بنجاح")

    # 4. المسار الثاني: صاحب المشروع (المراحل 7 - 8: تقديم طلب التمويل والرقابة الشرعية)
    prj_payload = {
        "title": "مصنع تحويل المنتجات الفلاحية بالجنوب",
        "sector": "industrial",
        "islamic_formula": "musharaka",
        "requested_amount": 1000000.0,
        "duration_months": 12,
        "expected_return_rate": 15.0,
        "description": "خط عصر وتعبئة زيت الزيتون وزيوت البذور الطبيعية",
        "guarantees": "رهن عقاري للمقر الصناعي"
    }
    r_prj = client.post("/api/projects/submit", headers=headers, json=prj_payload)
    assert r_prj.status_code == 200
    prj_id = r_prj.json()["project"]["id"]
    print(f"[8] رائد الأعمال قدّم طلب التمويل لمشروع رقم {prj_id}")

    # قرار الهيئة الشرعية المستقلة (المرحلة 8)
    r_sharia = client.post("/api/projects/sharia/decision", headers=headers, json={
        "project_id": prj_id,
        "is_approved": True,
        "sharia_scholar_name": "د. عبد الرحمن الجزائري",
        "notes": "المشروع مجاز شرعياً بالصيغة المحددة وفق المادة 78 من القانون 25-06.",
        "assigned_risk_grade": "LOW"
    })
    assert r_sharia.status_code == 200
    print("[9] الهيئة الشرعية المستقلة أجازت المشروع وطرحته للتمويل")

    # 5. المرحلة 10 و 11: التمويل من المحفظة الوقفية المستقلة ومن الممول الفردي
    # أ) تخصيص 60,000 د.ج من الوقف المستقل
    r_wf = client.post("/api/funding/fund-waqf", headers=headers, json={
        "project_id": prj_id,
        "waqf_fund_id": waqf_id,
        "amount": 60000.0
    })
    assert r_wf.status_code == 200
    print("[10] تم تخصيص 60,000 د.ج من الوقف المستقل وإيداعها في حساب الضمان للمشروع")

    # ب) تمويل 40,000 د.ج من الممول الفردي بماله الخاص
    r_if = client.post("/api/funding/fund-individual", headers=headers, json={
        "project_id": prj_id,
        "amount": 40000.0,
        "acknowledge_risk": True
    })
    assert r_if.status_code == 200
    print("[11] استثمر الممول الفردي 40,000 د.ج بماله الخاص مع توقيع عقد التمويل الإلكتروني")

    # 6. المرحلة 12: تحقيق العوائد والتسوية المالية والتوزيع
    # إيرادات: 300,000 د.ج ، تكاليف مباشرة: 100,000 د.ج -> صافي ربح 200,000 د.ج
    r_settle = client.post("/api/returns/execute-settlement", headers=headers, json={
        "project_id": prj_id,
        "gross_revenue": 300000.0,
        "direct_expenses": 100000.0,
        "auditor_name": "مكتب التدقيق المحاسبي المعتمد"
    })
    assert r_settle.status_code == 200, r_settle.text
    settle_data = r_settle.json()["settlement"]
    assert settle_data["waqf_gross_profit"] > 0
    assert settle_data["reserve_fund_deduction"] > 0
    assert settle_data["nazir_fee_deduction"] > 0
    assert settle_data["waqf_net_for_beneficiaries"] > 0
    print(f"[12] تمت التسوية المالية بنجاح:")
    print(f"     - أرباح الوقف الإجمالية: {settle_data['waqf_gross_profit']:,.2f} د.ج")
    print(f"     - استقطاع صندوق الاحتياطي (5%): {settle_data['reserve_fund_deduction']:,.2f} د.ج")
    print(f"     - اقتطاع أجرة الناظر (10%): {settle_data['nazir_fee_deduction']:,.2f} د.ج")
    print(f"     - الصافي المحول لجهات الوقف المستفيدة: {settle_data['waqf_net_for_beneficiaries']:,.2f} د.ج")

    # 7. المرحلة 13: الشفافية والمؤشرات المنشورة
    r_kpi = client.get("/api/governance/public-kpis")
    assert r_kpi.status_code == 200
    kpis = r_kpi.json()
    assert kpis["metrics"]["total_waqf_capital"] > 0
    assert kpis["metrics"]["total_returns_distributed_to_charities"] > 0
    print("[13] تم التحقق من نشر مؤشرات الأداء والشفافية للجمهور")
    print("--- اكتمل فحص جميع مراحل السيناريو بنجاح تام! ---\n")

if __name__ == "__main__":
    test_full_scenario_e2e()
