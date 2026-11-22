"""
نماذج الحوكمة والتدقيق الشرعي والمالي والشكاوى وسجل صندوق الاحتياطي
وفقاً للفصل الحادي عشر من القانون 25-06
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class AuditLog(BaseModel):
    """سجل المراجعة والتدقيق الإداري والمالي"""
    __tablename__ = "audit_logs"

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_type = Column(String(50), nullable=False) # CREATE_WAQF, KYC_VERIFY, SHARIA_APPROVE, DISBURSE, DISTRIBUTE
    entity_name = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=False)
    ip_address = Column(String(50), nullable=True)

class ShariaAuditReport(BaseModel):
    """تقرير التدقيق الشرعي الدوري الصادر عن الهيئة الشرعية المستقلة"""
    __tablename__ = "sharia_audit_reports"

    report_title = Column(String(200), nullable=False)
    quarter = Column(String(20), nullable=False) # Q1-2025, Q2-2025...
    compliance_verdict = Column(String(50), nullable=False) # FULLY_COMPLIANT, MINOR_OBSERVATIONS, VIOLATIONS_DETECTED
    auditor_names = Column(String(255), nullable=False)
    summary_findings = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=True)
    is_published = Column(Boolean, default=True) # ينشر للجمهور لتحقيق الشفافية

class ReserveFundLedger(BaseModel):
    """سجل حركات صندوق الاحتياطي الوقفي لمواجهة المخاطر"""
    __tablename__ = "reserve_fund_ledger"

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    transaction_type = Column(String(20), nullable=False) # INFLOW (تغذية من الأرباح), OUTFLOW (تخفيف خسارة)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)

class Complaint(BaseModel):
    """نموذج الشكاوى ومسار التحكيم وحل النزاعات"""
    __tablename__ = "complaints"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    complaint_code = Column(String(50), unique=True, index=True, nullable=False)
    subject = Column(String(200), nullable=False)
    details = Column(Text, nullable=False)
    category = Column(String(50), nullable=False) # FINANCIAL, SHARIA, CONTRACTUAL, TECHNICAL
    status = Column(String(30), default="OPEN")   # OPEN, UNDER_REVIEW, RESOLVED, ESCALATED_REGULATOR
    resolution_reply = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

