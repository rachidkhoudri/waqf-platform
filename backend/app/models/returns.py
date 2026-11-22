"""
نماذج تسوية العوائد وتوزيع الأرباح والخسائر وحصص المستفيدين وصندوق الاحتياطي وأجرة الناظر (10%)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class ProjectSettlement(BaseModel):
    """
    تسوية المشروع المالية:
    حساب الأرباح أو الخسائر الفعلية وفق الصيغة الإسلامية الخاصة بالمشروع
    بدون ضمان رأس المال، مع استقطاع صندوق الاحتياطي وأجرة الناظر (10%).
    """
    __tablename__ = "project_settlements"

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    settlement_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # الإيرادات والتكاليف المباشرة
    gross_revenue = Column(Float, nullable=False)        # إجمالي الإيرادات
    direct_expenses = Column(Float, nullable=False)      # التكاليف المباشرة المثبتة
    net_operating_result = Column(Float, nullable=False) # صافي النتيجة (ربح أو خسارة)
    is_loss = Column(Boolean, default=False)             # هل حقق المشروع خسارة؟
    loss_explanation = Column(Text, nullable=True)       # أسباب الخسارة (قضاء وقدر، جوائح، تعدي...)
    has_owner_misconduct = Column(Boolean, default=False)# هل ثبت تعدٍّ أو تفريط من صاحب المشروع؟

    # التوزيع حسب الصيغة الإسلامية المعتمدة
    project_owner_share = Column(Float, default=0.0)    # حصة رائد الأعمال
    total_funders_profit = Column(Float, default=0.0)   # إجمالي ربح جهات التمويل قبل الاستقطاعات
    
    # حصة الممولين الأفراد
    individual_funders_share = Column(Float, default=0.0)
    
    # حصة المحفظة الوقفية
    waqf_gross_profit = Column(Float, default=0.0)      # ربح الوقف الإجمالي
    reserve_fund_deduction = Column(Float, default=0.0) # استقطاع صندوق الاحتياطي الوقفي
    nazir_fee_deduction = Column(Float, default=0.0)    # استقطاع أجرة الناظر (10% من ربح الوقف)
    waqf_net_for_beneficiaries = Column(Float, default=0.0) # الصافي المحول لجهات الوقف المستفيدة

    # الحالة
    status = Column(String(30), default="CALCULATED")   # CALCULATED, AUDITED, DISTRIBUTED
    audited_by = Column(String(100), nullable=True)     # اسم المدقق المالي أو الخارجي
    audit_notes = Column(Text, nullable=True)

    project = relationship("Project", back_populates="settlements")
    disbursements = relationship("BeneficiaryDisbursement", back_populates="settlement", cascade="all, delete-orphan")

class BeneficiaryDisbursement(BaseModel):
    """
    صرف العوائد للجهات المستفيدة:
    تحويل ريع الوقف للجهات الثمانية وفق شرط كل واقف،
    مع اشتراط رفع تقرير الإنفاق السنوي من المؤسسة المستفيدة
    """
    __tablename__ = "beneficiary_disbursements"

    settlement_id = Column(Integer, ForeignKey("project_settlements.id"), nullable=False, index=True)
    waqf_fund_id = Column(Integer, ForeignKey("waqf_funds.id"), nullable=False, index=True)
    
    # الفئة المستفيدة من الفئات الثمانية
    category_id = Column(String(50), nullable=False)
    beneficiary_user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # حساب المؤسسة المستفيدة
    
    amount = Column(Float, nullable=False) # المبلغ المصروف بالدينار الجزائري
    disbursement_method = Column(String(50), default="BANK_TRANSFER") # تحويل بنكي إلى حساب المؤسسة
    transaction_ref = Column(String(100), nullable=False)
    
    status = Column(String(30), default="TRANSFERRED") # TRANSFERRED, CONFIRMED, IMPACT_REPORTED
    disbursed_at = Column(DateTime, default=datetime.utcnow)
    
    # تقرير الأثر والإنفاق الخيري
    impact_report_text = Column(Text, nullable=True)
    impact_report_url = Column(String(255), nullable=True)
    impact_report_submitted_at = Column(DateTime, nullable=True)

    settlement = relationship("ProjectSettlement", back_populates="disbursements")

