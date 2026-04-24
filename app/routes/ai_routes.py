from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services.space_object_service import generate_ai_description as space_ai
from app.services.plant_service import generate_ai_description as plant_ai
from app.utils.response import success, fail, error

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ai/space-object", methods=["POST", "OPTIONS"])
@cross_origin()
def generate_space_ai():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json()
    nama = data.get("nama")
    tipe = data.get("tipe")

    if not nama:
        return fail("Nama tidak boleh kosong", status_code=400)
    if not tipe:
        return fail("Tipe tidak boleh kosong", status_code=400)

    try:
        result = space_ai(nama, tipe)
        return success("Berhasil generate deskripsi AI", result)
    except Exception as e:
        return error(str(e))

@ai_bp.route("/ai/plant", methods=["POST", "OPTIONS"])
@cross_origin()
def generate_plant_ai():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json()
    nama = data.get("nama")

    if not nama:
        return fail("Nama tidak boleh kosong", status_code=400)

    try:
        result = plant_ai(nama)
        return success("Berhasil generate deskripsi AI", result)
    except Exception as e:
        return error(str(e))