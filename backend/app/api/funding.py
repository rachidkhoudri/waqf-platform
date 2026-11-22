"""
مسارات التمويل والتعاقد وحسابات الضمان للممولين وللمحفظة الوقفية
المراحل 10 و 11 من سيناريو وقف تاك
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.project import Project, ProjectMilestone
from app.models.funding import ProjectFunding
from app.models.waqf import WaqfFund
from app.api.auth import get_current_user
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/funding", tags=["التمويل والاستثمار والتعاقد"])

# ----------------- نماذج Pydantic -----------------
class IndividualFundRequest(BaseModel):
    project_id: int
    amount: float
    acknowledge_risk: bool # الإقرار بتحمل الخسارة المحتملة بدون ضمان رأس مال

class WaqfFundAllocationRequest(BaseModel):
    project_id: int
    waqf_fund_id: int
    amount: float

class MilestoneDisburseRequest(BaseModel):
    milestone_id: int
    inspector_notes: str

# ----------------- المسارات -----------------

@router.post("/fund-individual", summary="الخطوات 43 - 48: استثمار ممول فردي في مشروع وتوقيع العقد وإيداع الضمان")
def fund_as_individual(
    data: IndividualFundRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not data.acknowledge_risk:
        raise HTTPException(
            status_code=400,
            detail="يجب الإقرار شرعاً وقانوناً بأن رأس المال غير مضمون، وأنك تتحمل الخسارة المحتملة الناتجة عن نشاط المشروع وفق الصيغة الإسلامية."
        )

    # التحقق من صفة الممول
    if not current_user.is_funder and not current_user.is_admin:
        current_user.is_funder = True
        db.commit()

    try:
        funding = ProjectService.fund_project_with_individual(
            db=db,
            project_id=data.project_id,
            funder=current_user,
            amount=data.amount
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": f"تم توقيع عقد التمويل الإلكتروني بنجاح برقم ({funding.contract_number}) وتم إيداع المبلغ في حساب الضمان.",
        "funding": {
            "id": funding.id,
            "contract_number": funding.contract_number,
            "escrow_account": funding.escrow_account_num,
            "amount": funding.amount,
            "status": funding.status
        }
    }

@router.post("/fund-waqf", summary="تخصيص استثمار من المحفظة الوقفية المستقلة لمشروع معتمد")
def fund_from_waqf(
    data: WaqfFundAllocationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """المنصة بصفتها الناظر (أو الواقف صاحب الوقف المستقل) تخصص حصة من الوقف في المشروع"""
    waqf_fund = db.query(WaqfFund).filter(WaqfFund.id == data.waqf_fund_id).first()
    if not waqf_fund:
        raise HTTPException(status_code=404, detail="الوقف المستقل غير موجود")
    if waqf_fund.waqif_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="غير مصرح لك بإدارة هذا الوقف")

    try:
        funding = ProjectService.fund_project_with_waqf(
            db=db,
            project_id=data.project_id,
            waqf_fund_id=data.waqf_fund_id,
            allocation_amount=data.amount
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": f"تم تخصيص مبلغ {data.amount:,.2f} د.ج من وقفك المستقل للاستثمار في المشروع بنجاح.",
        "funding": {
            "id": funding.id,
            "contract_number": funding.contract_number,
            "escrow_account": funding.escrow_account_num,
            "amount": funding.amount
        }
    }

@router.post("/disburse-milestone", summary="الخطوة 49: صرف دفعة مرحلية للمشروع بعد معاينة الإنجاز الميداني")
def disburse_milestone(
    data: MilestoneDisburseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """إدارة المنصة أو مفتش الأوقاف المعتمد يعاين المرحلة ويحرر الدفعة من حساب الضمان"""
    milestone = db.query(ProjectMilestone).filter(ProjectMilestone.id == data.milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="المرحلة غير موجودة")

    project = db.query(Project).filter(Project.id == milestone.project_id).first()

    milestone.status = "DISBURSED"
    milestone.inspection_notes = data.inspector_notes or "تمت المعاينة والتحقق من شراء الأصول/الإنجاز الفعلي وفق المواصفات."
    milestone.inspected_at = milestone.created_at # تاريخ المعاينة
    
    # تحديث نسبة إنجاز المشروع الكلية
    project.execution_progress_pct = max(project.execution_progress_pct, milestone.target_progress_pct)
    if project.status == "FUNDED":
        project.status = "IN_EXECUTION"

    db.commit()

    return {
        "success": True,
        "message": f"تم تحرير الدفعة البالغة {milestone.disbursement_amount:,.2f} د.ج من حساب الضمان لصالح المشروع بنجاح.",
        "current_progress": project.execution_progress_pct
    }

@router.get("/my-investments", summary="الخطوة 50 - 51: قائمة الاستثمارات ومتابعة تقدم المشاريع للممول")
def get_my_investments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fundings = db.query(ProjectFunding).filter(
        (ProjectFunding.funder_id == current_user.id) | 
        (ProjectFunding.waqf_fund_id.in_([f.id for f in current_user.waqf_funds]))
    ).order_by(ProjectFunding.created_at.desc()).all()

    results = []
    for f in fundings:
        project = f.project
        results.append({
            "funding_id": f.id,
            "funding_source": f.funding_source,
            "amount": f.amount,
            "contract_number": f.contract_number,
            "status": f.status,
            "created_at": f.created_at.strftime('%Y-%m-%d'),
            "project": {
                "id": project.id,
                "title": project.title,
                "sector": project.sector,
                "formula": project.islamic_formula,
                "expected_return_rate": project.expected_return_rate,
                "status": project.status,
                "progress_pct": project.execution_progress_pct
            }
        })

    return results

