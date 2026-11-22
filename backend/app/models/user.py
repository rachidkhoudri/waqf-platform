"""
نموذج المستخدمين وإدارة الهوية والتحقق (KYC/AML) والأدوار في منصة وقف تاك
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.database import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    # البيانات الأساسية (المرحلة 1)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(30), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # حالة التفعيل والأمان
    is_active = Column(Boolean, default=True)
    is_phone_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=True)
    
    # التحقق من الهوية KYC (الخطوة 6 و 7)
    kyc_status = Column(String(30), default="PENDING")  # PENDING, APPROVED, REJECTED
    kyc_id_type = Column(String(50), nullable=True)     # بطاقة التعريف البيومترية، جواز السفر
    kyc_id_number = Column(String(100), nullable=True)
    kyc_id_doc_url = Column(String(255), nullable=True) # مسار وثيقة الهوية
    kyc_selfie_url = Column(String(255), nullable=True) # مسار الصورة الشخصية
    kyc_submitted_at = Column(DateTime, nullable=True)
    kyc_reviewed_at = Column(DateTime, nullable=True)
    kyc_notes = Column(Text, nullable=True)

    # الأدوار الخمسة المنفصلة (المرحلة 2)
    is_waqif = Column(Boolean, default=False)           # حساب واقف
    is_funder = Column(Boolean, default=False)          # حساب ممول فردي
    is_project_owner = Column(Boolean, default=False)   # حساب صاحب مشروع (رائد أعمال)
    is_beneficiary = Column(Boolean, default=False)     # حساب جهة مستفيدة
    is_admin = Column(Boolean, default=False)           # ناظر الوقف / إدارة المنصة
    is_sharia_board = Column(Boolean, default=False)    # عضو الهيئة الشرعية المستقلة

    # متطلبات دور الواقف: مكافحة غسل الأموال (قانون 05-01 وقانون 25-06)
    aml_declaration_accepted = Column(Boolean, default=False)
    aml_source_of_funds = Column(String(255), nullable=True)

    # متطلبات دور الممول: فحص الملاءمة وتحمل المخاطر
    funder_risk_profile = Column(String(50), default="MEDIUM") # LOW, MEDIUM, HIGH
    funder_max_limit = Column(Float, default=1000000.0)        # سقف التمويل الأقصى المسموح بالدينار الجزائري

    # متطلبات دور صاحب المشروع: السجل التجاري والوضعية الضريبية
    company_name = Column(String(200), nullable=True)
    commercial_register_num = Column(String(100), nullable=True)
    tax_id_num = Column(String(100), nullable=True)
    business_license_url = Column(String(255), nullable=True)

    # متطلبات دور الجهة المستفيدة: وثائق الاعتماد القانوني والحساب البنكي
    organization_name = Column(String(200), nullable=True)
    legal_approval_number = Column(String(100), nullable=True)
    bank_account_rip = Column(String(50), nullable=True) # الرقم التعريفي البنكي الجزائري RIP/IBAN
    beneficiary_category = Column(String(50), nullable=True) # إحدى الفئات الثمانية
    is_vetted_beneficiary = Column(Boolean, default=False)

    # العلاقات
    waqf_funds = relationship("WaqfFund", back_populates="waqif", foreign_keys="WaqfFund.waqif_id")
    projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    fundings = relationship("ProjectFunding", back_populates="funder", foreign_keys="ProjectFunding.funder_id")
    notifications = relationship("Notification", back_populates="user")

