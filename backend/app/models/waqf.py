"""
نماذج الأوقاف المستقلة، الإيداعات، الشروط، والعقود الإلكترونية
وفقاً للقانون الجزائري 25-06
"""
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import BaseModel
from app.config import settings

class WaqfFund(BaseModel):
    """
    الوقف المستقل لكل واقف:
    لكل واقف ذمة وقفية ومحفظة مستقلة بحساباتها وأرقامها،
    مع المحافظة على أصل رأس المال وعدم صرفه (المادة 33)
    """
    __tablename__ = "waqf_funds"

    waqif_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    waqf_code = Column(String(50), unique=True, index=True, nullable=False) # رمز الوقف مثلاً: WQF-DZ-2025-XXXX
    waqf_title = Column(String(200), nullable=False) # اسم الوقف، مثلاً: وقف الصدقة الجارية، وقف الوالدين

    # نوع الوقف: مؤبد أو مؤقت (وفق المادة 22 من القانون 25-06)
    waqf_type = Column(String(20), default="PERPETUAL", nullable=False) # PERPETUAL (مؤبد), TEMPORARY (مؤقت)
    temporary_duration_months = Column(Integer, nullable=True)          # مدة الوقف المؤقت بالشهور
    temporary_end_date = Column(DateTime, nullable=True)                # تاريخ انتهاء الوقف المؤقت ومصير الأصل
    temporary_capital_destination = Column(String(200), nullable=True)  # مصير الأصل بعد انقضاء الأجل (يعاد للواقف أو لورثته)

    # المبالغ المحاسبية المفصولة
    capital_corpus = Column(Float, default=0.0, nullable=False)         # أصل المبلغ الوقفي (محبّس ومصون لا يُصرف)
    current_invested_amount = Column(Float, default=0.0, nullable=False)# الجزء المستثمر في المشاريع
    uninvested_cash = Column(Float, default=0.0, nullable=False)        # السيولة النقدية الجاهزة في حساب الوقف
    total_returns_earned = Column(Float, default=0.0, nullable=False)   # إجمالي العوائد المحققة تاريخياً
    total_returns_distributed = Column(Float, default=0.0, nullable=False) # إجمالي ما تم تحويله للجهات المستفيدة

    # الحالة وفترة المراجعة (72 ساعة)
    # PENDING_COOLING_OFF (في فترة المراجعة 72 ساعة)، ACTIVE (أصبح لازماً بعد 72 ساعة)، CANCELLED (تراجع)، COMPLETED (انتهى المؤقت)
    status = Column(String(30), default="PENDING_COOLING_OFF", nullable=False)
    cooling_off_expires_at = Column(DateTime, nullable=False)
    can_withdraw_now = Column(Boolean, default=True)

    # نمط المخاطرة المفضل للواقف
    risk_preference = Column(String(30), default="CONSERVATIVE") # CONSERVATIVE (مرابحة وإجارة), BALANCED (شراكات ومضاربة)

    # شرط تعذر الصرف (المادة 35 من القانون 25-06: التحويل لأقرب جهة مستحقة)
    cy_pres_accepted = Column(Boolean, default=True)

    # العلاقات
    waqif = relationship("User", back_populates="waqf_funds", foreign_keys=[waqif_id])
    deposits = relationship("WaqfDeposit", back_populates="waqf_fund", cascade="all, delete-orphan")
    conditions = relationship("WaqfCondition", back_populates="waqf_fund", cascade="all, delete-orphan")
    contracts = relationship("WaqfContract", back_populates="waqf_fund", cascade="all, delete-orphan")
    fundings = relationship("ProjectFunding", back_populates="waqf_fund")

class WaqfDeposit(BaseModel):
    """
    سجل عمليات الإيداع في الوقف المستقل
    """
    __tablename__ = "waqf_deposits"

    waqf_fund_id = Column(Integer, ForeignKey("waqf_funds.id"), nullable=False, index=True)
    waqif_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False) # بالدينار الجزائري
    payment_method = Column(String(50), nullable=False) # CIB_CARD (بطاقة بنكية CIB), EDAHABIA (الذهبية), BANK_TRANSFER (تحويل بنكي)
    transaction_ref = Column(String(100), unique=True, index=True, nullable=False)
    payment_status = Column(String(30), default="SUCCESS") # PENDING, SUCCESS, FAILED, REFUNDED
    is_refunded_cooling_off = Column(Boolean, default=False)
    receipt_doc_url = Column(String(255), nullable=True)

    waqf_fund = relationship("WaqfFund", back_populates="deposits")

class WaqfCondition(BaseModel):
    """
    شرط الوقف والجهات المستفيدة من أرباح الوقف فقط:
    توزيع العوائد على الفئات الثمانية أو جهات محددة مع تحديد النسب والشروط الإضافية
    """
    __tablename__ = "waqf_conditions"

    waqf_fund_id = Column(Integer, ForeignKey("waqf_funds.id"), nullable=False, index=True)
    category_id = Column(String(50), nullable=False) # education, health, environment, ... (من الفئات الثمانية)
    specific_beneficiary_id = Column(Integer, ForeignKey("users.id"), nullable=True) # مؤسسة معينة معتمدة إن وجدت
    
    percentage = Column(Float, nullable=False) # نسبة التوزيع (مثلاً 50.0%)
    
    # شروط إضافية
    geographic_scope = Column(String(100), nullable=True) # مثلاً: ولاية معينة في الجزائر أو عموم الوطن
    target_demographic = Column(String(150), nullable=True) # مثلاً: أيتام القرى النائية، طلبة الطب
    custom_condition_notes = Column(Text, nullable=True)

    waqf_fund = relationship("WaqfFund", back_populates="conditions")

class WaqfContract(BaseModel):
    """
    عقد الوقف الإلكتروني الرسمي:
    يوضح أن المنصة هي ناظر الوقف، وأصل الوقف مصون لا يستهلك،
    والأرباح فقط للجهات المستفيدة، مع التوقيع الإلكتروني والشهادة.
    """
    __tablename__ = "waqf_contracts"

    waqf_fund_id = Column(Integer, ForeignKey("waqf_funds.id"), nullable=False, unique=True)
    waqif_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    contract_number = Column(String(100), unique=True, index=True, nullable=False)
    contract_title = Column(String(255), nullable=False)
    contract_text_ar = Column(Text, nullable=False)
    
    signed_electronically = Column(Boolean, default=False)
    signed_at = Column(DateTime, nullable=True)
    signer_ip_address = Column(String(50), nullable=True)
    certificate_code = Column(String(100), unique=True, nullable=True) # رمز شهادة الوقف الإلكترونية
    pdf_path = Column(String(255), nullable=True)

    waqf_fund = relationship("WaqfFund", back_populates="contracts")

