"""
نماذج تمويل المشاريع من المصدرين: المحفظة الوقفية المستقلة، والممولين الأفراد
وحسابات الضمان (Escrow)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class ProjectFunding(BaseModel):
    """
    سجل التمويل: يوثق مساهمة الوقف أو الممول في مشروع معين،
    مع ضمان فصل الحسابات محاسبياً وقانونياً
    """
    __tablename__ = "project_fundings"

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # نوع مصدر التمويل: WAQF (محفظة وقفية مستقلة) أو INDIVIDUAL (ممول فردي)
    funding_source = Column(String(30), nullable=False) # WAQF, INDIVIDUAL
    
    waqf_fund_id = Column(Integer, ForeignKey("waqf_funds.id"), nullable=True, index=True)
    funder_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    amount = Column(Float, nullable=False) # المبلغ المموّل بالدينار الجزائري
    
    # نسبة توزيع الأرباح التعاقدية حسب الصيغة
    agreed_profit_share_pct = Column(Float, nullable=False) # حصة الممول من أرباح المشروع
    
    # التعاقد الإلكتروني
    contract_number = Column(String(100), unique=True, index=True, nullable=False)
    contract_signed = Column(Boolean, default=False)
    contract_signed_at = Column(DateTime, nullable=True)
    contract_text_ar = Column(Text, nullable=True)

    # حساب الضمان المنفصل للمشروع (Escrow Account)
    escrow_account_num = Column(String(100), nullable=False)
    funds_in_escrow = Column(Boolean, default=True)
    
    # الحالة
    status = Column(String(30), default="COMMITTED") # COMMITTED, IN_ESCROW, DISBURSED_TO_PROJECT, COMPLETED

    # العلاقات
    project = relationship("Project", back_populates="fundings")
    waqf_fund = relationship("WaqfFund", back_populates="fundings", foreign_keys=[waqf_fund_id])
    funder = relationship("User", back_populates="fundings", foreign_keys=[funder_id])

