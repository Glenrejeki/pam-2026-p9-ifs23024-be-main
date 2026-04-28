from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime, timezone
from app.extensions import Base

class Motivation(Base):
    __tablename__ = "motivations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    request_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "request_id": self.request_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
