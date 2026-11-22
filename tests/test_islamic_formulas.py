"""
اختبارات محرك الحسابات للصيغ الإسلامية السبع المعتمدة في القانون الجزائري 25-06
بدون ضمان رأس المال، مع استقطاع أجرة الناظر (10%) وصندوق الاحتياطي (5%).
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.services.islamic_formulas import IslamicFormulaEngine

def test_musharaka_profit():
    # مشروع مشاركة حقق ربحاً
    res = IslamicFormulaEngine.calculate_settlement(
        formula="musharaka",
        total_project_capital=2000000.0,
        waqf_capital=1000000.0,
        individual_funder_capital=500000.0,
        owner_capital=500000.0,
        gross_revenue=3000000.0,
        direct_expenses=2000000.0, # صافي الربح 1,000,000
        agreed_profit_sharing_ratio=0.70, # 70% لحملة المال و 30% لرائد الأعمال
        nazir_fee_rate=0.10,
        reserve_fund_rate=0.05
    )
    assert res["net_operating"] == 1000000.0
    assert res["owner_share"] == 300000.0
    assert res["total_funders_share"] == 700000.0
    # الوقف يمثل ثلثي رأس مال الممولين (1M من 1.5M)
    assert round(res["waqf_gross_share"], 2) == round(700000.0 * (1.0 / 1.5), 2)
    assert res["reserve_fund_deduction"] > 0
    assert res["nazir_fee_deduction"] > 0
    assert res["waqf_net_for_beneficiaries"] > 0
    print("[PASS] test_musharaka_profit")

def test_musharaka_loss_shared_by_capital():
    # في المشاركة: الخسارة تكون بقدر حصة كل طرف في رأس المال حصراً
    res = IslamicFormulaEngine.calculate_settlement(
        formula="musharaka",
        total_project_capital=2000000.0,
        waqf_capital=1000000.0,           # 50% من رأس المال
        individual_funder_capital=500000.0, # 25% من رأس المال
        owner_capital=500000.0,            # 25% من رأس المال
        gross_revenue=1000000.0,
        direct_expenses=1400000.0, # خسارة 400,000
        agreed_profit_sharing_ratio=0.60
    )
    assert res["is_loss"] is True
    assert res["loss_borne_by_waqf"] == 200000.0      # 50%
    assert res["loss_borne_by_funders"] == 100000.0   # 25%
    assert res["loss_borne_by_owner"] == 100000.0     # 25%
    assert res["waqf_net_for_beneficiaries"] == 0.0
    print("[PASS] test_musharaka_loss_shared_by_capital")

def test_mudaraba_no_capital_guarantee():
    # في المضاربة: الخسارة المالية على رب المال دون ضمان لرأس المال
    res = IslamicFormulaEngine.calculate_settlement(
        formula="mudaraba",
        total_project_capital=1000000.0,
        waqf_capital=1000000.0,
        individual_funder_capital=0.0,
        owner_capital=0.0,
        gross_revenue=700000.0,
        direct_expenses=900000.0, # خسارة 200,000
        agreed_profit_sharing_ratio=0.50,
        has_misconduct=False
    )
    assert res["is_loss"] is True
    assert res["loss_borne_by_waqf"] == 200000.0
    assert res["loss_borne_by_owner"] == 0.0 # المضارب خسر جهده
    print("[PASS] test_mudaraba_no_capital_guarantee")

def test_mudaraba_misconduct_liability():
    # إذا ثبت تعدٍّ أو تفريط من المضارب فيضمن الخسارة
    res = IslamicFormulaEngine.calculate_settlement(
        formula="mudaraba",
        total_project_capital=1000000.0,
        waqf_capital=1000000.0,
        individual_funder_capital=0.0,
        owner_capital=0.0,
        gross_revenue=700000.0,
        direct_expenses=900000.0,
        agreed_profit_sharing_ratio=0.50,
        has_misconduct=True
    )
    assert res["is_loss"] is True
    assert res["loss_borne_by_owner"] == 200000.0 # يضمنها المضارب
    print("[PASS] test_mudaraba_misconduct_liability")

def test_murabaha_margin():
    # المرابحة: بيع بربح معلوم
    res = IslamicFormulaEngine.calculate_settlement(
        formula="murabaha",
        total_project_capital=1000000.0,
        waqf_capital=1000000.0,
        individual_funder_capital=0.0,
        owner_capital=0.0,
        gross_revenue=1200000.0,
        direct_expenses=1000000.0, # هامش ربح 200,000
        agreed_profit_sharing_ratio=1.0,
        nazir_fee_rate=0.10,
        reserve_fund_rate=0.05
    )
    assert res["total_funders_share"] == 200000.0
    assert res["reserve_fund_deduction"] == 10000.0 # 5% of 200k
    assert res["nazir_fee_deduction"] == 19000.0   # 10% of 190k
    assert res["waqf_net_for_beneficiaries"] == 171000.0
    print("[PASS] test_murabaha_margin")

if __name__ == "__main__":
    test_musharaka_profit()
    test_musharaka_loss_shared_by_capital()
    test_mudaraba_no_capital_guarantee()
    test_mudaraba_misconduct_liability()
    test_murabaha_margin()
    print("ALL ISLAMIC FORMULA TESTS PASSED SUCCESSFULLY!")

