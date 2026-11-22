"""
تجميع كافة النماذج لقاعدة بيانات وقف تاك
"""
from app.database import Base, BaseModel
from app.models.user import User
from app.models.waqf import WaqfFund, WaqfDeposit, WaqfCondition, WaqfContract
from app.models.project import Project, ProjectMilestone
from app.models.funding import ProjectFunding
from app.models.returns import ProjectSettlement, BeneficiaryDisbursement
from app.models.audit import AuditLog, ShariaAuditReport, ReserveFundLedger, Complaint
from app.models.notification import Notification

__all__ = [
    "Base",
    "BaseModel",
    "User",
    "WaqfFund",
    "WaqfDeposit",
    "WaqfCondition",
    "WaqfContract",
    "Project",
    "ProjectMilestone",
    "ProjectFunding",
    "ProjectSettlement",
    "BeneficiaryDisbursement",
    "AuditLog",
    "ShariaAuditReport",
    "ReserveFundLedger",
    "Complaint",
    "Notification"
]

