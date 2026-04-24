from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime, timezone
from app.extensions import Base
import uuid

class Plant(Base):
    __tablename__ = "plants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nama = Column(String(100), nullable=False)
    path_gambar = Column(String(255), nullable=False)
    deskripsi = Column(Text, nullable=False)
    manfaat = Column(Text, nullable=False)
    efek_samping = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))