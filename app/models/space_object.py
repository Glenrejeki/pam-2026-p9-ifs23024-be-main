from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime, timezone
from app.extensions import Base
import uuid

class SpaceObject(Base):
    __tablename__ = "space_objects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nama = Column(String(100), nullable=False)
    tipe = Column(String(50), nullable=False)
    path_gambar = Column(String(255), nullable=False)
    deskripsi = Column(Text, nullable=False)
    jarak_dari_bumi = Column(String(100), nullable=False)
    fakta = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))