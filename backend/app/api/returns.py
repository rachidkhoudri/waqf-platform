"""
مسارات التسوية المالية وتوزيع الأرباح والشفافية وتقارير الأثر للمستفيدين
المرحلة 12 والمرحلة 13 من سيناريو وقف تاك
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings, WAQF_CATEGORIES
from app.models.user import User
from app.models.project import Project
from app.models.returns import ProjectSettlement, BeneficiaryDisbursement
from app.api.auth import get_current_user
from app.services.returns_service import ReturnsService

router = APIRouter(prefix="/api/returns", tags=["التسويات والعوائد وتوزيع الأرباح"])

# ----------------- نماذج Pydantic -----------------
class ExecuteSettlementRequest(BaseModel):
    project_id: int
    gross_revenue: float
    direct_expenses: float
    auditor_name: str
    has_misconduct: bool = False # هل ثبت تعدٍّ أو تفريط من صاحب المشروع؟
    audit_notes: Optional[str] = "تم التدقيق المالي ومطابقة الفواتير والسجلات التشغيلية للمشروع."

class SubmitImpactReportRequest(BaseModel):
    disbursement_id: int
    impact_report_text: str
    impact_report_url: Optional[str] = "docs/impact_report_2025.pdf"

# ----------------- المسارات -----------------

@router.post("/execute-settlement", summary="الخطوات 52 - 58: تنفيذ التسوية المالية وتوزيع الأرباح واقتطاع أجرة الناظر (10%)")
def execute_settlement(
    data: ExecuteSettlementRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    المنصة كناظر ومدقق مالي:
    1. تجميع العوائد وخصم التكاليف المباشرة
    2. الحساب حسب الصيغة الإسلامية السبعة المعتمدة
    3. حفظ أصل الوقف وإعادته لرصيد الوقف المستقل
    4. تخصيص حصة الممول الفردي
    5. استقطاع صندوق الاحتياطي الوقفي
    6. اقتطاع أجرة الناظر (10% المحددة لصالح المنصة)
    7. توزيع الصافي على الجهات المستفيدة للوقف وفق شرط الواقف
    8. إشعار جميع الأطراف
    """
    try:
        settlement = ReturnsService.execute_project_settlement(
            db=db,
            project_id=data.project_id,
            gross_revenue=data.gross_revenue,
            direct_expenses=data.direct_expenses,
            auditor_name=data.auditor_name,
            has_misconduct=data.has_misconduct,
            audit_notes=data.audit_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": "تمت التسوية المالية وتوزيع الأرباح واستقطاع أجرة الناظر (10%) وصندوق الاحتياطي وتحويل الريع للمستحقين بنجاح.",
        "settlement": {
            "id": settlement.id,
            "project_id": settlement.project_id,
            "gross_revenue": settlement.gross_revenue,
            "direct_expenses": settlement.direct_expenses,
            "net_operating": settlement.net_operating_result,
            "is_loss": settlement.is_loss,
            "project_owner_share": settlement.project_owner_share,
            "individual_funders_share": settlement.individual_funders_share,
            "waqf_gross_profit": settlement.waqf_gross_profit,
            "reserve_fund_deduction": settlement.reserve_fund_deduction,
            "nazir_fee_deduction": settlement.nazir_fee_deduction,
            "waqf_net_for_beneficiaries": settlement.waqf_net_for_beneficiaries
        }
    }

@router.get("/project/{project_id}", summary="سجل تسوية المشروع وتفاصيل التوزيع")
def get_project_settlement(project_id: int, db: Session = Depends(get_db)):
    settlement = db.query(ProjectSettlement).filter(ProjectSettlement.project_id == project_id).first()
    if not settlement:
        raise HTTPException(status_code=404, detail="لم يتم إجراء تسوية لهذا المشروع بعد.")

    disbursements = db.query(BeneficiaryDisbursement).filter(BeneficiaryDisbursement.settlement_id == settlement.id).all()

    return {
        "settlement_id": settlement.id,
        "settlement_date": settlement.settlement_date.strftime('%Y-%m-%d %H:%M'),
        "gross_revenue": settlement.gross_revenue,
        "direct_expenses": settlement.direct_expenses,
        "net_operating": settlement.net_operating_result,
        "is_loss": settlement.is_loss,
        "loss_explanation": settlement.loss_explanation,
        "project_owner_share": settlement.project_owner_share,
        "individual_funders_share": settlement.individual_funders_share,
        "waqf_gross_profit": settlement.waqf_gross_profit,
        "reserve_fund_deduction": settlement.reserve_fund_deduction,
        "nazir_fee_deduction": settlement.nazir_fee_deduction,
        "waqf_net_for_beneficiaries": settlement.waqf_net_for_beneficiaries,
        "audited_by": settlement.audited_by,
        "audit_notes": settlement.audit_notes,
        "beneficiary_disbursements": [
            {
                "id": d.id,
                "waqf_fund_id": d.waqf_fund_id,
                "category_id": d.category_id,
                "category_name": WAQF_CATEGORIES.get(d.category_id, {}).get("name", d.category_id),
                "amount": d.amount,
                "status": d.status,
                "disbursed_at": d.disbursed_at.strftime('%Y-%m-%d'),
                "has_impact_report": bool(d.impact_report_text)
            }
            for d in disbursements
        ]
    }

@router.post("/beneficiary/submit-impact-report", summary="تقديم تقرير الإنفاق والأثر الخيري من الجهة المستفيدة")
def submit_impact_report(
    data: SubmitImpactReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """الجهات المستفيدة ملزمة برفع تقرير الإنفاق الشفاف لضمان استمرار إدراجها"""
    disbursement = db.query(BeneficiaryDisbursement).filter(BeneficiaryDisbursement.id == data.disbursement_id).first()
    if not disbursement:
        raise HTTPException(status_code=404, detail="سجل الصرف غير موجود.")

    disbursement.impact_report_text = data.impact_report_text
    disbursement.impact_report_url = data.impact_report_url
    disbursement.impact_report_submitted_at = disbursement.created_at # تاريخ التقديم
    disbursement.status = "IMPACT_REPORTED"

    db.commit()

    return {
        "success": True,
        "message": "تم استلام تقرير الإنفاق والأثر المجتمعي بنجاح، وسينشر في لوحة متابعة الواقفين لتعزيز الشفافية."
    }

