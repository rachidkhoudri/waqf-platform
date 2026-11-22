"""
مسارات الحوكمة والشفافية ومؤشرات الأداء العامة وقناة الشكاوى
الخطوات 59 - 63 من سيناريو وقف تاك
"""
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.config import settings, WAQF_CATEGORIES, INVESTMENT_SECTORS, ISLAMIC_FINANCING_FORMULAS
from app.models.user import User
from app.models.waqf import WaqfFund
from app.models.project import Project
from app.models.funding import ProjectFunding
from app.models.returns import ProjectSettlement, BeneficiaryDisbursement
from app.models.audit import ShariaAuditReport, ReserveFundLedger, Complaint
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/governance", tags=["الحوكمة والشفافية والشكاوى"])

# ----------------- نماذج Pydantic -----------------
class FileComplaintRequest(BaseModel):
    subject: str
    details: str
    category: str # FINANCIAL, SHARIA, CONTRACTUAL, TECHNICAL

class PublishShariaReportRequest(BaseModel):
    report_title: str
    quarter: str
    compliance_verdict: str
    auditor_names: str
    summary_findings: str
    recommendations: Optional[str] = None

# ----------------- المسارات -----------------

@router.get("/public-kpis", summary="الخطوات 59 و 60: مؤشرات الأداء والشفافية المنشورة للجمهور")
def get_public_kpis(db: Session = Depends(get_db)):
    """
    نشر مؤشرات الأداء العامة على الموقع الإلكتروني:
    - حجم الأموال الوقفية
    - العائد الموزع على المستحقين
    - رصيد صندوق الاحتياطي الوقفي
    - أجرة الناظر الفعلية المحصلة (10%)
    - عدد المشاريع المستثمرة
    - عدد المستفيدين من الفئات الثمانية
    """
    total_waqf_capital = db.query(func.sum(WaqfFund.capital_corpus)).scalar() or 0.0
    total_distributed = db.query(func.sum(BeneficiaryDisbursement.amount)).scalar() or 0.0
    total_nazir_fees = db.query(func.sum(ProjectSettlement.nazir_fee_deduction)).scalar() or 0.0
    total_reserve_fund = db.query(func.sum(ProjectSettlement.reserve_fund_deduction)).scalar() or 0.0
    
    total_waqf_count = db.query(WaqfFund).count()
    total_projects = db.query(Project).count()
    active_investments = db.query(Project).filter(Project.status.in_(["IN_EXECUTION", "FUNDED"])).count()
    completed_projects = db.query(Project).filter(Project.status == "COMPLETED").count()
    total_beneficiaries_served = db.query(BeneficiaryDisbursement).count()

    # توزيع حسب الفئات الوقفية الثمانية
    category_distribution = {}
    for cat_id, cat_data in WAQF_CATEGORIES.items():
        cat_amount = db.query(func.sum(BeneficiaryDisbursement.amount)).filter(BeneficiaryDisbursement.category_id == cat_id).scalar() or 0.0
        category_distribution[cat_id] = {
            "name": cat_data["name"],
            "amount_distributed": cat_amount
        }

    return {
        "platform_name": settings.PLATFORM_NAME,
        "law_reference": settings.LAW_REFERENCE,
        "currency": settings.CURRENCY_AR,
        "metrics": {
            "total_waqf_capital": total_waqf_capital,
            "total_returns_distributed_to_charities": total_distributed,
            "total_reserve_fund_balance": total_reserve_fund,
            "total_nazir_fees_collected_10pct": total_nazir_fees,
            "total_independent_waqf_accounts": total_waqf_count,
            "total_projects": total_projects,
            "active_investments": active_investments,
            "completed_projects": completed_projects,
            "beneficiary_disbursements_count": total_beneficiaries_served
        },
        "waqf_categories_impact": category_distribution,
        "governance_principles": [
            "فصل حسابات أموال الوقف عن حسابات المنصة التشغيلية وحسابات الممولين",
            "إلغاء ضمان رأس المال عملاً بأحكام الشريعة الإسلامية ومبدأ الغنم بالغرم",
            "هيئة شرعية مستقلة تصدر قراراتها كتابياً وتراجع كافة المشاريع والصيغ",
            "صندوق احتياطي وقفي يخفف مخاطر الاستثمار",
            "أجرة ناظر شفافة وثابتة بنسبة 10% من صافي الأرباح المحققة فقط"
        ]
    }

@router.get("/sharia-reports", summary="الخطوة 61: تقارير التدقيق الشرعي والمالي الدورية")
def list_sharia_audit_reports(db: Session = Depends(get_db)):
    reports = db.query(ShariaAuditReport).filter(ShariaAuditReport.is_published == True).order_by(ShariaAuditReport.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "title": r.report_title,
            "quarter": r.quarter,
            "compliance_verdict": r.compliance_verdict,
            "auditors": r.auditor_names,
            "findings": r.summary_findings,
            "recommendations": r.recommendations,
            "published_at": r.created_at.strftime('%Y-%m-%d')
        }
        for r in reports
    ]

@router.post("/complaints/submit", summary="تقديم شكوى أو طلب تحكيم عبر التطبيق")
def submit_complaint(
    data: FileComplaintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint_code = f"CMP-DZ-{uuid.uuid4().hex[:8].upper()}"
    complaint = Complaint(
        user_id=current_user.id,
        complaint_code=complaint_code,
        subject=data.subject,
        details=data.details,
        category=data.category,
        status="OPEN"
    )
    db.add(complaint)
    db.commit()

    return {
        "success": True,
        "message": f"تم استلام شكواك برقم تتبع ({complaint_code}). سيتم دراستها من لجنة الحوكمة والرد خلال 5 أيام عمل.",
        "complaint_code": complaint_code
    }

