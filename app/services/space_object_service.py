from app.extensions import SessionLocal
from app.models.space_object import SpaceObject
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response
from app.config import Config
from datetime import datetime, timezone
import os
import uuid

def build_image_url(path_gambar):
    return f"{Config.BASE_URL}/static/{path_gambar.replace('uploads/', '')}"

def to_dict(obj):
    return {
        "id": obj.id,
        "nama": obj.nama,
        "tipe": obj.tipe,
        "pathGambar": obj.path_gambar,
        "gambar": build_image_url(obj.path_gambar),
        "deskripsi": obj.deskripsi,
        "jarakDariBumi": obj.jarak_dari_bumi,
        "fakta": obj.fakta,
        "createdAt": obj.created_at.isoformat() if obj.created_at else None,
        "updatedAt": obj.updated_at.isoformat() if obj.updated_at else None,
    }

def get_all_space_objects(search="", tipe=""):
    session = SessionLocal()
    try:
        query = session.query(SpaceObject)
        if search:
            query = query.filter(SpaceObject.nama.ilike(f"%{search}%"))
        if tipe:
            query = query.filter(SpaceObject.tipe == tipe)
        return [to_dict(o) for o in query.order_by(SpaceObject.created_at.desc()).limit(20)]
    finally:
        session.close()

def get_space_object_by_id(id):
    session = SessionLocal()
    try:
        obj = session.query(SpaceObject).filter(SpaceObject.id == id).first()
        return to_dict(obj) if obj else None
    finally:
        session.close()

def get_space_object_by_name(nama):
    session = SessionLocal()
    try:
        return session.query(SpaceObject).filter(SpaceObject.nama == nama).first()
    finally:
        session.close()

def create_space_object(data, file=None):
    session = SessionLocal()
    try:
        path_gambar = ""
        if file:
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            path_gambar = f"uploads/space/{filename}"
            file.save(path_gambar)

        obj = SpaceObject(
            id=str(uuid.uuid4()),
            nama=data.get("nama", "").strip(),
            tipe=data.get("tipe", "").strip(),
            path_gambar=path_gambar,
            deskripsi=data.get("deskripsi", ""),
            jarak_dari_bumi=data.get("jarakDariBumi", "").strip(),
            fakta=data.get("fakta", ""),
        )
        session.add(obj)
        session.commit()
        return obj.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_space_object(id, data, file=None):
    session = SessionLocal()
    try:
        obj = session.query(SpaceObject).filter(SpaceObject.id == id).first()
        if not obj:
            return False

        if file:
            # Hapus file lama
            if obj.path_gambar and os.path.exists(obj.path_gambar):
                os.remove(obj.path_gambar)
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            obj.path_gambar = f"uploads/space/{filename}"
            file.save(obj.path_gambar)

        obj.nama = data.get("nama", obj.nama).strip()
        obj.tipe = data.get("tipe", obj.tipe).strip()
        obj.deskripsi = data.get("deskripsi", obj.deskripsi)
        obj.jarak_dari_bumi = data.get("jarakDariBumi", obj.jarak_dari_bumi).strip()
        obj.fakta = data.get("fakta", obj.fakta)
        obj.updated_at = datetime.now(timezone.utc)

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_space_object(id):
    session = SessionLocal()
    try:
        obj = session.query(SpaceObject).filter(SpaceObject.id == id).first()
        if not obj:
            return False
        if obj.path_gambar and os.path.exists(obj.path_gambar):
            os.remove(obj.path_gambar)
        session.delete(obj)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def generate_ai_description(nama, tipe):
    prompt = f"""
    Dalam format JSON, buat deskripsi lengkap untuk objek luar angkasa "{nama}" dengan tipe "{tipe}".
    Format:
    {{
        "deskripsi": "...",
        "fakta": "...",
        "jarakDariBumi": "..."
    }}
    """
    result = generate_from_llm(prompt)
    return parse_llm_response(result)