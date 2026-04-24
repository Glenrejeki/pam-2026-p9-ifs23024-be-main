from app.extensions import SessionLocal
from app.models.plant import Plant
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response
from app.config import Config
from datetime import datetime, timezone
import os
import uuid

def build_image_url(path_gambar):
    return f"{Config.BASE_URL}/static/{path_gambar.replace('uploads/', '')}"

def to_dict(plant):
    return {
        "id": plant.id,
        "nama": plant.nama,
        "pathGambar": plant.path_gambar,
        "gambar": build_image_url(plant.path_gambar),
        "deskripsi": plant.deskripsi,
        "manfaat": plant.manfaat,
        "efekSamping": plant.efek_samping,
        "createdAt": plant.created_at.isoformat() if plant.created_at else None,
        "updatedAt": plant.updated_at.isoformat() if plant.updated_at else None,
    }

def get_all_plants(search=""):
    session = SessionLocal()
    try:
        query = session.query(Plant)
        if search:
            query = query.filter(Plant.nama.ilike(f"%{search}%"))
        return [to_dict(p) for p in query.order_by(Plant.created_at.desc()).limit(20)]
    finally:
        session.close()

def get_plant_by_id(id):
    session = SessionLocal()
    try:
        plant = session.query(Plant).filter(Plant.id == id).first()
        return to_dict(plant) if plant else None
    finally:
        session.close()

def get_plant_by_name(nama):
    session = SessionLocal()
    try:
        return session.query(Plant).filter(Plant.nama == nama).first()
    finally:
        session.close()

def create_plant(data, file=None):
    session = SessionLocal()
    try:
        path_gambar = ""
        if file:
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            path_gambar = f"uploads/plants/{filename}"
            file.save(path_gambar)

        plant = Plant(
            id=str(uuid.uuid4()),
            nama=data.get("nama", "").strip(),
            path_gambar=path_gambar,
            deskripsi=data.get("deskripsi", ""),
            manfaat=data.get("manfaat", ""),
            efek_samping=data.get("efekSamping", ""),
        )
        session.add(plant)
        session.commit()
        return plant.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_plant(id, data, file=None):
    session = SessionLocal()
    try:
        plant = session.query(Plant).filter(Plant.id == id).first()
        if not plant:
            return False

        if file:
            if plant.path_gambar and os.path.exists(plant.path_gambar):
                os.remove(plant.path_gambar)
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            plant.path_gambar = f"uploads/plants/{filename}"
            file.save(plant.path_gambar)

        plant.nama = data.get("nama", plant.nama).strip()
        plant.deskripsi = data.get("deskripsi", plant.deskripsi)
        plant.manfaat = data.get("manfaat", plant.manfaat)
        plant.efek_samping = data.get("efekSamping", plant.efek_samping)
        plant.updated_at = datetime.now(timezone.utc)

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_plant(id):
    session = SessionLocal()
    try:
        plant = session.query(Plant).filter(Plant.id == id).first()
        if not plant:
            return False
        if plant.path_gambar and os.path.exists(plant.path_gambar):
            os.remove(plant.path_gambar)
        session.delete(plant)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def generate_ai_description(nama):
    prompt = f"""
    Dalam format JSON, buat deskripsi lengkap untuk tumbuhan "{nama}".
    Format:
    {{
        "deskripsi": "...",
        "manfaat": "...",
        "efekSamping": "..."
    }}
    """
    result = generate_from_llm(prompt)
    return parse_llm_response(result)