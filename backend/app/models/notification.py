"""
نموذج الإشعارات والتنبيهات الفورية للمستخدمين
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="INFO") # INFO, SUCCESS, WARNING, PROFIT_DISTRIBUTION, CONTRACT
    action_url = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")

