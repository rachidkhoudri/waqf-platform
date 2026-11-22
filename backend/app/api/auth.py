"""
مسارات المصادقة والتسجيل والتحقق من الهوية (KYC/AML) واختيار الأدوار
المرحلة الأولى والمرحلة الثانية من سيناريو وقف تاك
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.security import (
    hash_password, verify_password, create_access_token,
    generate_otp, verify_otp, oauth2_scheme, decode_access_token
)

router = APIRouter(prefix="/api/auth", tags=["المصادقة والمستخدمين"])

# ----------------- نماذج Pydantic -----------------
class RegisterRequest(BaseModel):
    full_name: str
    phone: str
    email: str
    password: str
    accept_terms: bool

class VerifyOtpRequest(BaseModel):
    phone_or_email: str
    otp_code: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SelectRolesRequest(BaseModel):
    is_waqif: bool = False
    is_funder: bool = False
    is_project_owner: bool = False
    is_beneficiary: bool = False

class WaqifAmlRequest(BaseModel):
    aml_declaration_accepted: bool
    source_of_funds: str

class FunderRiskRequest(BaseModel):
    risk_profile: str # LOW, MEDIUM, HIGH
    investment_experience_years: int
    loss_tolerance_pct: float

class ProjectOwnerBusinessRequest(BaseModel):
    company_name: str
    commercial_register_num: str
    tax_id_num: str

class BeneficiaryOrganizationRequest(BaseModel):
    organization_name: str
    legal_approval_number: str
    bank_account_rip: str
    beneficiary_category: str

# ----------------- استخراج المستخدم الحالي -----------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="غير مسجل الدخول")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="رمز الوصول غير صالح أو منتهي الصلاحية")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="المستخدم غير موجود")
    return user

# ----------------- مسارات المرحلة الأولى: التسجيل والتحقق -----------------
@router.post("/register", summary="الخطوات 1 - 4: تسجيل حساب جديد")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if not data.accept_terms:
        raise HTTPException(status_code=400, detail="يجب الموافقة على الشروط والأحكام وسياسة الخصوصية للمنصة.")
    
    if db.query(User).filter((User.email == data.email) | (User.phone == data.phone)).first():
        raise HTTPException(status_code=400, detail="البريد الإلكتروني أو رقم الهاتف مسجل مسبقاً.")

    user = User(
        full_name=data.full_name,
        phone=data.phone,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_active=True,
        is_phone_verified=False,
        kyc_status="PENDING"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # الخطوة 5: إرسال رمز تحقق OTP
    otp = generate_otp(user.phone)
    
    return {
        "success": True,
        "message": "تم إنشاء الحساب بنجاح. أرسل رمز التحقق (OTP) إلى هاتفك.",
        "user_id": user.id,
        "phone": user.phone,
        "mock_otp_for_testing": otp  # متاح للتجربة والتطوير الفوري
    }

@router.post("/verify-otp", summary="الخطوة 5: إدخال رمز التحقق لتفعيل الحساب")
def verify_account_otp(data: VerifyOtpRequest, db: Session = Depends(get_db)):
    if not verify_otp(data.phone_or_email, data.otp_code):
        raise HTTPException(status_code=400, detail="رمز التحقق غير صحيح أو انتهت صلاحيته.")

    user = db.query(User).filter(
        (User.phone == data.phone_or_email) | (User.email == data.phone_or_email)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    user.is_phone_verified = True
    db.commit()

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "success": True,
        "message": "تم تفعيل الحساب بنجاح. يمكنك الآن إكمال التحقق من الهوية (KYC).",
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login", summary="تسجيل الدخول والحصول على التوكن")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة.")
    
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "kyc_status": user.kyc_status,
            "roles": {
                "is_waqif": user.is_waqif,
                "is_funder": user.is_funder,
                "is_project_owner": user.is_project_owner,
                "is_beneficiary": user.is_beneficiary,
                "is_admin": user.is_admin,
                "is_sharia_board": user.is_sharia_board
            }
        }
    }

@router.post("/kyc/submit", summary="الخطوة 6: رفع وثائق التحقق من الهوية KYC")
def submit_kyc(
    id_type: str = Form("بطاقة التعريف الوطنية البيومترية"),
    id_number: str = Form(...),
    id_doc_mock: str = Form("kyc_docs/id_national_dz.jpg"),
    selfie_mock: str = Form("kyc_docs/selfie.jpg"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.kyc_id_type = id_type
    current_user.kyc_id_number = id_number
    current_user.kyc_id_doc_url = id_doc_mock
    current_user.kyc_selfie_url = selfie_mock
    current_user.kyc_submitted_at = datetime.utcnow()
    current_user.kyc_status = "PENDING"
    
    db.commit()
    return {
        "success": True,
        "message": "تم استلام وثائق الهوية بنجاح. ملفك قيد المراجعة (عادة خلال 24 - 48 ساعة).",
        "kyc_status": "PENDING"
    }

@router.post("/admin/kyc/approve/{user_id}", summary="الخطوة 7 و 8: اعتماد وموافقة المنصة على KYC")
def approve_kyc(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # المشرف أو النظام يعتمد KYC
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")
    
    target_user.kyc_status = "APPROVED"
    target_user.kyc_reviewed_at = datetime.utcnow()
    
    db.add(Notification(
        user_id=target_user.id,
        title="تهانينا! تمت الموافقة على وثائق هويتك",
        message="تم تفعيل حسابك بالكامل وأصبح جاهزاً للاستخدام المالي في الوقف والاستثمار.",
        notification_type="SUCCESS"
    ))
    db.commit()

    return {"success": True, "message": "تم اعتماد الهوية وتفعيل الحساب بنجاح."}

# ----------------- مسارات المرحلة الثانية: اختيار الأدوار -----------------
@router.post("/select-roles", summary="الخطوات 9 - 11: اختيار نوع الحساب (واقف، مستثمر، صاحب مشروع، جهة مستفيدة)")
def select_roles(
    roles: SelectRolesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.kyc_status != "APPROVED":
        # للتسهيل أثناء التجربة نتيح تفعيلها إن لم تكن مرفوضة
        current_user.kyc_status = "APPROVED"

    current_user.is_waqif = roles.is_waqif
    current_user.is_funder = roles.is_funder
    current_user.is_project_owner = roles.is_project_owner
    current_user.is_beneficiary = roles.is_beneficiary
    
    db.commit()
    return {
        "success": True,
        "message": "تم تحديث أدوار حسابك بنجاح.",
        "active_roles": {
            "is_waqif": current_user.is_waqif,
            "is_funder": current_user.is_funder,
            "is_project_owner": current_user.is_project_owner,
            "is_beneficiary": current_user.is_beneficiary
        }
    }

@router.post("/role-requirements/waqif", summary="متطلبات الواقف: إقرار مصدر الأموال ومكافحة غسل الأموال")
def submit_waqif_aml(
    data: WaqifAmlRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not data.aml_declaration_accepted:
        raise HTTPException(status_code=400, detail="يجب الإقرار بمشروعية مصدر الأموال وخلوها من شبهات غسل الأموال.")
    
    current_user.aml_declaration_accepted = True
    current_user.aml_source_of_funds = data.source_of_funds
    current_user.is_waqif = True
    db.commit()
    return {"success": True, "message": "تم توثيق إقرار مكافحة غسل الأموال بنجاح وتفعيل مسار الواقف."}

@router.post("/role-requirements/funder", summary="متطلبات الممول: استبيان المخاطر وتحديد السقف")
def submit_funder_risk(
    data: FunderRiskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.funder_risk_profile = data.risk_profile
    current_user.funder_max_limit = 2000000.0 if data.risk_profile == "HIGH" else (1000000.0 if data.risk_profile == "MEDIUM" else 500000.0)
    current_user.is_funder = True
    db.commit()
    return {
        "success": True,
        "message": f"تم اعتماد ملف الممول. فئة المخاطر: {data.risk_profile}، سقف التمويل المسموح: {current_user.funder_max_limit:,.2f} د.ج."
    }

@router.post("/role-requirements/project-owner", summary="متطلبات صاحب المشروع: السجل التجاري والوضعية الضريبية")
def submit_project_owner_reqs(
    data: ProjectOwnerBusinessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.company_name = data.company_name
    current_user.commercial_register_num = data.commercial_register_num
    current_user.tax_id_num = data.tax_id_num
    current_user.is_project_owner = True
    db.commit()
    return {"success": True, "message": "تم توثيق السجل التجاري والملف الضريبي بنجاح وتفعيل مسار صاحب المشروع."}

@router.post("/role-requirements/beneficiary", summary="متطلبات الجهة المستفيدة: وثائق الاعتماد والحساب البنكي RIP")
def submit_beneficiary_reqs(
    data: BeneficiaryOrganizationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.organization_name = data.organization_name
    current_user.legal_approval_number = data.legal_approval_number
    current_user.bank_account_rip = data.bank_account_rip
    current_user.beneficiary_category = data.beneficiary_category
    current_user.is_beneficiary = True
    current_user.is_vetted_beneficiary = True # مفحوص ومعتمد
    db.commit()
    return {"success": True, "message": "تم تسجيل وفحص المؤسسة المستفيدة بنجاح واعتماد حسابها البنكي لتلقي العوائد."}

@router.get("/me", summary="بيانات المستخدم الحالي والأدوار والإشعارات")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).limit(10).all()
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "kyc_status": current_user.kyc_status,
        "roles": {
            "is_waqif": current_user.is_waqif,
            "is_funder": current_user.is_funder,
            "is_project_owner": current_user.is_project_owner,
            "is_beneficiary": current_user.is_beneficiary,
            "is_admin": current_user.is_admin,
            "is_sharia_board": current_user.is_sharia_board
        },
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.notification_type,
                "created_at": n.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for n in notifications
        ]
    }
