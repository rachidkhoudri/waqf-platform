"""
نماذج مشاريع الاستثمار، مراحل الصرف، والدراسة الشرعية والفنية
وفقاً للقطاعات الخمسة والصيغ الشرعية السبع في القانون 25-06
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class Project(BaseModel):
    """
    مشروع استثماري يطلبه رائد الأعمال (صاحب المشروع)
    ويمر بمراحل: العناية الواجبة -> الرقابة الشرعية -> تصنيف المخاطر -> الطرح للتمويل
    """
    __tablename__ = "projects"

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # القطاع الاستثماري (القطاعات الخمسة)
    # industrial, commercial, agricultural, services, infrastructure
    sector = Column(String(50), nullable=False)
    
    # الصيغة الإسلامية المقترحة والمعتمدة (الصيغ السبع)
    # musharaka, mudaraba, murabaha, salam, istisna, ijarah, muzaraa
    islamic_formula = Column(String(50), nullable=False)
    
    # البيانات المالية والتشغيلية
    requested_amount = Column(Float, nullable=False)    # المبلغ المطلوب بالدينار الجزائري
    funded_amount = Column(Float, default=0.0)          # المبلغ المموّل فعلياً حتى الآن
    duration_months = Column(Integer, nullable=False)   # مدة التنفيذ أو الاستثمار
    expected_return_rate = Column(Float, nullable=False)# نسبة العائد السنوي المتوقع (غير مضمون شرعاً)
    expected_return_min = Column(Float, nullable=True)  # أدنى عائد متوقع
    expected_return_max = Column(Float, nullable=True)  # أقصى عائد متوقع

    # الضمانات المشروعة ودراسات الجدوى
    guarantees_description = Column(Text, nullable=True) # رهن، كفالة تجارية، شيك ضمان التزام
    feasibility_study_url = Column(String(255), nullable=True)
    financial_statements_url = Column(String(255), nullable=True)

    # تصنيف المخاطر والحالة
    # SUBMITTED (جديد), DUE_DILIGENCE (دراسة فنية), SHARIA_REVIEW (هيئة شرعية),
    # APPROVED_FOR_FUNDING (معتمد مطروح), FUNDED (اكتمل التمويل), IN_EXECUTION (قيد الإنجاز),
    # COMPLETED (منجز وتم توزيع الأرباح), REJECTED (مرفوض مسبباً)
    status = Column(String(50), default="SUBMITTED", nullable=False)
    risk_grade = Column(String(20), default="MEDIUM") # LOW (منخفضة), MEDIUM (متوسطة), HIGH (مرتفعة)

    # قرار الهيئة الشرعية المستقلة
    sharia_status = Column(String(30), default="PENDING") # PENDING, APPROVED, REJECTED, CONDITIONAL
    sharia_decision_date = Column(DateTime, nullable=True)
    sharia_opinion_text = Column(Text, nullable=True)
    sharia_scholar_signature = Column(String(100), nullable=True)

    # قرار الإدارة والتحقق الفني
    technical_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # المتابعة والإنجاز
    execution_progress_pct = Column(Float, default=0.0) # نسبة التقدم الميداني 0 - 100%
    is_returns_distributed = Column(Boolean, default=False)

    # العلاقات
    owner = relationship("User", back_populates="projects", foreign_keys=[owner_id])
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")
    fundings = relationship("ProjectFunding", back_populates="project", cascade="all, delete-orphan")
    settlements = relationship("ProjectSettlement", back_populates="project", cascade="all, delete-orphan")

class ProjectMilestone(BaseModel):
    """
    مراحل إنجاز المشروع: لا يصرف التمويل دفعة واحدة،
    بل على دفعات مرتبطة بمراحل إنجاز يتحقق منها مفتشو المنصة (المادة 99 و 102)
    """
    __tablename__ = "project_milestones"

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    milestone_number = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    target_progress_pct = Column(Float, nullable=False) # نسبة الإنجاز المطلوبة لصرف الدفعة
    disbursement_amount = Column(Float, nullable=False) # مبلغ الدفعة بالدينار الجزائري
    
    status = Column(String(30), default="PENDING") # PENDING, VERIFIED, DISBURSED
    inspection_notes = Column(Text, nullable=True)
    inspected_at = Column(DateTime, nullable=True)
    disbursed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="milestones")

