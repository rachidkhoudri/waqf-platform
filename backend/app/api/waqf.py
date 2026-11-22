"""
مسارات حساب الواقف: الإيداع، تحديد الشروط، التعاقد الإلكتروني، والشهادات
المراحل 3، 4، 5، و 6 من سيناريو وقف تاك
"""
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings, WAQF_CATEGORIES
from app.models.user import User
from app.models.waqf import WaqfFund, WaqfDeposit, WaqfCondition, WaqfContract
from app.api.auth import get_current_user
from app.services.waqf_service import WaqfService

router = APIRouter(prefix="/api/waqf", tags=["مسار الواقف والأوقاف"])

# ----------------- نماذج Pydantic -----------------
class ConditionItem(BaseModel):
    category_id: str
    specific_beneficiary_id: Optional[int] = None
    percentage: float
    geographic_scope: Optional[str] = "كافة التراب الوطني الجزائري"
    target_demographic: Optional[str] = None
    custom_condition_notes: Optional[str] = None

class CreateWaqfRequest(BaseModel):
    waqf_title: str
    amount: float
    payment_method: str # CIB_CARD, EDAHABIA, BANK_TRANSFER
    waqf_type: str = "PERPETUAL" # PERPETUAL, TEMPORARY
    temporary_months: Optional[int] = None
    temporary_destination: Optional[str] = None
    risk_preference: str = "CONSERVATIVE" # CONSERVATIVE, BALANCED
    conditions: List[ConditionItem]

# ----------------- المسارات -----------------

@router.get("/categories", summary="قائمة الفئات الوقفية الثمانية المعتمدة")
def get_waqf_categories():
    """عرض المجالات الوقفية الثمانية المحددة في الخطوة 18"""
    return list(WAQF_CATEGORIES.values())

@router.post("/create", summary="الخطوات 12 - 26: إيداع وقف جديد وتحديد الشروط وتوقيع العقد الإلكتروني")
def create_waqf(
    data: CreateWaqfRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    تنفيذ المراحل الثالثة والرابعة والخامسة بالكامل:
    - إيداع المبلغ بالعملة المحلية (د.ج)
    - اختيار طريقة الدفع (CIB، الذهبية، تحويل بنكي)
    - اختيار الفئات المستفيدة من القائمة الثمانية مع نسب التوزيع والشروط الإضافية
    - تحديد نوع الوقف (مؤبد أو مؤقت) ومستوى المخاطرة
    - إنشاء وتوقيع عقد الوقف الإلكتروني
    - بدء سريان فترة التراجع (72 ساعة)
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    conditions_dict = [c.dict() for c in data.conditions]

    try:
        waqf_fund = WaqfService.create_independent_waqf(
            db=db,
            waqif=current_user,
            waqf_title=data.waqf_title,
            amount=data.amount,
            payment_method=data.payment_method,
            waqf_type=data.waqf_type,
            temporary_months=data.temporary_months,
            temporary_destination=data.temporary_destination,
            conditions_data=conditions_dict,
            risk_preference=data.risk_preference,
            client_ip=client_ip
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    contract = db.query(WaqfContract).filter(WaqfContract.waqf_fund_id == waqf_fund.id).first()

    return {
        "success": True,
        "message": f"تم تسجيل وإيداع وقفك المستقل بنجاح برقم ({waqf_fund.waqf_code}). لديك 72 ساعة كفترة تراجع قانونية.",
        "waqf_fund": {
            "id": waqf_fund.id,
            "waqf_code": waqf_fund.waqf_code,
            "title": waqf_fund.waqf_title,
            "capital_corpus": waqf_fund.capital_corpus,
            "waqf_type": waqf_fund.waqf_type,
            "status": waqf_fund.status,
            "cooling_off_expires_at": waqf_fund.cooling_off_expires_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
            "contract_number": contract.contract_number if contract else None,
            "certificate_code": contract.certificate_code if contract else None
        }
    }

@router.get("/my-funds", summary="الخطوة 27 - 28: قائمة الأوقاف المستقلة الخاصة بالواقف ومتابعة الأداء")
def get_my_waqf_funds(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    funds = db.query(WaqfFund).filter(WaqfFund.waqif_id == current_user.id).order_by(WaqfFund.created_at.desc()).all()
    
    results = []
    for f in funds:
        # تحديث حالة فترة الـ 72 ساعة تلقائياً
        WaqfService.check_and_update_cooling_off(db, f)
        
        contract = db.query(WaqfContract).filter(WaqfContract.waqf_fund_id == f.id).first()
        conditions = db.query(WaqfCondition).filter(WaqfCondition.waqf_fund_id == f.id).all()
        
        results.append({
            "id": f.id,
            "waqf_code": f.waqf_code,
            "title": f.waqf_title,
            "waqf_type": f.waqf_type,
            "capital_corpus": f.capital_corpus,
            "current_invested_amount": f.current_invested_amount,
            "uninvested_cash": f.uninvested_cash,
            "total_returns_earned": f.total_returns_earned,
            "total_returns_distributed": f.total_returns_distributed,
            "status": f.status,
            "can_withdraw_now": f.can_withdraw_now,
            "cooling_off_expires_at": f.cooling_off_expires_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
            "contract_number": contract.contract_number if contract else None,
            "certificate_code": contract.certificate_code if contract else None,
            "created_at": f.created_at.strftime('%Y-%m-%d'),
            "conditions": [
                {
                    "category_id": c.category_id,
                    "category_name": WAQF_CATEGORIES.get(c.category_id, {}).get("name", c.category_id),
                    "percentage": c.percentage,
                    "geographic_scope": c.geographic_scope
                }
                for c in conditions
            ]
        })
    return results

@router.get("/fund/{fund_id}/contract", summary="الخطوة 26: قراءة وتحميل عقد الوقف الإلكتروني")
def get_waqf_contract(fund_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    waqf = db.query(WaqfFund).filter(WaqfFund.id == fund_id).first()
    if not waqf:
        raise HTTPException(status_code=404, detail="الوقف غير موجود.")
    if waqf.waqif_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="غير مصرح لك بالاطلاع على هذا العقد.")

    contract = db.query(WaqfContract).filter(WaqfContract.waqf_fund_id == waqf.id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="عقد الوقف غير محرر.")

    return {
        "contract_number": contract.contract_number,
        "contract_title": contract.contract_title,
        "contract_text": contract.contract_text_ar,
        "signed_at": contract.signed_at.strftime('%Y-%m-%d %H:%M:%S UTC') if contract.signed_at else None,
        "certificate_code": contract.certificate_code,
        "signer_name": current_user.full_name
    }

@router.get("/fund/{fund_id}/certificate", summary="الخطوة 30: تحميل شهادة الوقف الإلكترونية الرسمية")
def get_waqf_certificate(fund_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    waqf = db.query(WaqfFund).filter(WaqfFund.id == fund_id).first()
    if not waqf:
        raise HTTPException(status_code=404, detail="الوقف غير موجود.")
    if waqf.waqif_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="غير مصرح لك.")

    contract = db.query(WaqfContract).filter(WaqfContract.waqf_fund_id == waqf.id).first()

    return {
        "certificate_title": "شهادة ثبوت وقف نقدي استثماري",
        "certificate_code": contract.certificate_code if contract else "CERT-WQF-PENDING",
        "waqif_name": current_user.full_name,
        "waqf_title": waqf.waqf_title,
        "waqf_code": waqf.waqf_code,
        "amount": waqf.capital_corpus,
        "currency": settings.CURRENCY_AR,
        "waqf_type": "مؤبد" if waqf.waqf_type == "PERPETUAL" else f"مؤقت ({waqf.temporary_duration_months} شهر)",
        "created_date": waqf.created_at.strftime('%Y-%m-%d'),
        "legal_reference": settings.LAW_REFERENCE,
        "supervised_by": f"{settings.PLATFORM_NAME} (الناظر المعتمد)"
    }

@router.post("/fund/{fund_id}/withdraw-cooling-off", summary="سحب المبلغ كاملاً وإلغاء الوقف خلال فترة الـ 72 ساعة")
def withdraw_waqf_cooling_off(
    fund_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        res = WaqfService.withdraw_cooling_off(db, waqf_fund_id=fund_id, waqif_id=current_user.id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

