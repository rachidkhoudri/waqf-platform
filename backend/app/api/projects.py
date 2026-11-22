"""
مسارات المشاريع والفرص الاستثمارية والرقابة الشرعية
المراحل 7، 8، و 9 من سيناريو وقف تاك
"""
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings, INVESTMENT_SECTORS, ISLAMIC_FINANCING_FORMULAS
from app.models.user import User
from app.models.project import Project, ProjectMilestone
from app.api.auth import get_current_user
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["المشاريع والفرص الاستثمارية"])

# ----------------- نماذج Pydantic -----------------
class MilestoneInput(BaseModel):
    title: str
    description: Optional[str] = None
    target_progress_pct: float
    disbursement_amount: float

class SubmitProjectRequest(BaseModel):
    title: str
    description: str
    sector: str # industrial, commercial, agricultural, services, infrastructure
    islamic_formula: str # musharaka, mudaraba, murabaha, salam, istisna, ijarah, muzaraa
    requested_amount: float
    duration_months: int
    expected_return_rate: float
    guarantees: Optional[str] = "كفالة تجارية ورهن أصول تشغيلية"
    milestones: Optional[List[MilestoneInput]] = None

class ShariaReviewDecisionRequest(BaseModel):
    project_id: int
    is_approved: bool
    sharia_scholar_name: str
    notes: str
    assigned_risk_grade: str = "MEDIUM" # LOW, MEDIUM, HIGH

# ----------------- المسارات -----------------

@router.get("/meta", summary="بيانات القطاعات الخمسة والصيغ الإسلامية السبع المعتمدة")
def get_investment_metadata():
    return {
        "sectors": INVESTMENT_SECTORS,
        "islamic_formulas": ISLAMIC_FINANCING_FORMULAS
    }

@router.post("/submit", summary="الخطوات 31 - 34: تقديم طلب تمويل مشروع جديد")
def submit_project(
    data: SubmitProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """صاحب المشروع يقدم الطلب مع الصيغة المقترحة والبيانات الفنية والضمانات"""
    if not current_user.is_project_owner and not current_user.is_admin:
        # تفعيل دور صاحب المشروع تلقائياً لتسهيل الاستخدام
        current_user.is_project_owner = True
        db.commit()

    milestones_data = [m.dict() for m in data.milestones] if data.milestones else None

    try:
        project = ProjectService.submit_project(
            db=db,
            owner=current_user,
            title=data.title,
            description=data.description,
            sector=data.sector,
            islamic_formula=data.islamic_formula,
            requested_amount=data.requested_amount,
            duration_months=data.duration_months,
            expected_return_rate=data.expected_return_rate,
            guarantees=data.guarantees,
            milestones_data=milestones_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": f"تم استلام طلب تمويل مشروعك بنجاح برقم ({project.project_code}). الطلب معروض الآن على الفحص الفني والهيئة الشرعية.",
        "project": {
            "id": project.id,
            "project_code": project.project_code,
            "title": project.title,
            "sector": project.sector,
            "formula": project.islamic_formula,
            "status": project.status
        }
    }

@router.get("/opportunities", summary="الخطوات 40 - 42: عرض المشاريع المعتمدة في قسم الفرص الاستثمارية")
def list_investment_opportunities(
    sector: Optional[str] = None,
    formula: Optional[str] = None,
    risk: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """تصفح المشاريع المعتمدة شرعياً والمطروحة للتمويل من الممولين والمحفظة الوقفية"""
    query = db.query(Project).filter(Project.status.in_(["APPROVED_FOR_FUNDING", "PARTIALLY_FUNDED"]))
    
    if sector:
        query = query.filter(Project.sector == sector)
    if formula:
        query = query.filter(Project.islamic_formula == formula)
    if risk:
        query = query.filter(Project.risk_grade == risk)

    projects = query.order_by(Project.created_at.desc()).all()

    results = []
    for p in projects:
        formula_info = ISLAMIC_FINANCING_FORMULAS.get(p.islamic_formula, {})
        remaining_to_fund = max(0.0, p.requested_amount - p.funded_amount)
        progress_funded_pct = round((p.funded_amount / p.requested_amount) * 100, 1) if p.requested_amount > 0 else 0

        results.append({
            "id": p.id,
            "project_code": p.project_code,
            "title": p.title,
            "description": p.description,
            "sector": p.sector,
            "sector_name": INVESTMENT_SECTORS.get(p.sector, {}).get("name", p.sector),
            "islamic_formula": p.islamic_formula,
            "formula_name": formula_info.get("name", p.islamic_formula),
            "legal_article": formula_info.get("legal_article", "قانون الأوقاف 25-06"),
            "loss_bearer_rule": formula_info.get("loss_bearer", ""),
            "requested_amount": p.requested_amount,
            "funded_amount": p.funded_amount,
            "remaining_amount": remaining_to_fund,
            "progress_funded_pct": progress_funded_pct,
            "duration_months": p.duration_months,
            "expected_return_rate": p.expected_return_rate,
            "risk_grade": p.risk_grade,
            "guarantees": p.guarantees_description,
            "sharia_opinion": p.sharia_opinion_text,
            "capital_guarantee_warning": "تنبيه شرعي وقانوني: العائد المتوقع غير مضمون، وأصل رأس المال يتحمل مخاطر الاستثمار المشروعة."
        })

    return results

@router.get("/detail/{project_id}", summary="تفاصيل المشروع والجدول الزمني ومراحل الصرف")
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")

    formula_info = ISLAMIC_FINANCING_FORMULAS.get(project.islamic_formula, {})
    milestones = db.query(ProjectMilestone).filter(ProjectMilestone.project_id == project.id).order_by(ProjectMilestone.milestone_number.asc()).all()

    return {
        "id": project.id,
        "project_code": project.project_code,
        "title": project.title,
        "description": project.description,
        "sector": project.sector,
        "sector_name": INVESTMENT_SECTORS.get(project.sector, {}).get("name", project.sector),
        "islamic_formula": project.islamic_formula,
        "formula_name": formula_info.get("name", project.islamic_formula),
        "legal_article": formula_info.get("legal_article", ""),
        "nature": formula_info.get("nature", ""),
        "return_source": formula_info.get("return_source", ""),
        "loss_bearer": formula_info.get("loss_bearer", ""),
        "requested_amount": project.requested_amount,
        "funded_amount": project.funded_amount,
        "duration_months": project.duration_months,
        "expected_return_rate": project.expected_return_rate,
        "risk_grade": project.risk_grade,
        "status": project.status,
        "guarantees": project.guarantees_description,
        "sharia_opinion": project.sharia_opinion_text,
        "sharia_scholar_signature": project.sharia_scholar_signature,
        "sharia_decision_date": project.sharia_decision_date.strftime('%Y-%m-%d') if project.sharia_decision_date else None,
        "execution_progress_pct": project.execution_progress_pct,
        "milestones": [
            {
                "id": m.id,
                "number": m.milestone_number,
                "title": m.title,
                "description": m.description,
                "target_progress_pct": m.target_progress_pct,
                "disbursement_amount": m.disbursement_amount,
                "status": m.status
            }
            for m in milestones
        ]
    }

@router.get("/sharia/pending", summary="المشاريع بانتظار قرار الهيئة الشرعية")
def list_pending_sharia(db: Session = Depends(get_db)):
    """قائمة المشاريع قيد المراجعة الشرعية"""
    projects = db.query(Project).filter(Project.sharia_status == "PENDING").all()
    return [
        {
            "id": p.id,
            "project_code": p.project_code,
            "title": p.title,
            "sector": p.sector,
            "formula": p.islamic_formula,
            "requested_amount": p.requested_amount,
            "duration_months": p.duration_months,
            "guarantees": p.guarantees_description
        }
        for p in projects
    ]

@router.post("/sharia/decision", summary="الخطوة 36 - 39: إصدار قرار الهيئة الشرعية المستقلة")
def decide_sharia_review(
    data: ShariaReviewDecisionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        project = ProjectService.approve_sharia_review(
            db=db,
            project_id=data.project_id,
            sharia_scholar_name=data.sharia_scholar_name,
            is_approved=data.is_approved,
            notes=data.notes,
            assigned_risk_grade=data.assigned_risk_grade
        )
        return {
            "success": True,
            "message": f"تم تسجيل قرار الهيئة الشرعية للمشروع ({project.project_code}) بنجاح.",
            "status": project.status,
            "sharia_status": project.sharia_status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

