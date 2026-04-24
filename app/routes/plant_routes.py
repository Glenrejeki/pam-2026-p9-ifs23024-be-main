from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
from app.services import plant_service
from app.utils.response import success, fail, error
from app.utils.validator import ValidatorHelper
import os

plant_bp = Blueprint("plant", __name__)

@plant_bp.route("/plants", methods=["GET", "OPTIONS"])
@cross_origin()
def get_all():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    search = request.args.get("search", "")
    data = plant_service.get_all_plants(search)
    return success("Berhasil mengambil daftar tumbuhan", {"plants": data})

@plant_bp.route("/plants/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def get_by_id(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    plant = plant_service.get_plant_by_id(id)
    if not plant:
        return fail("Data tumbuhan tidak tersedia!", status_code=404)
    return success("Berhasil mengambil data tumbuhan", {"plant": plant})

@plant_bp.route("/plants", methods=["POST", "OPTIONS"])
@cross_origin()
def create():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.form.to_dict()
    file = request.files.get("gambar")

    validator = ValidatorHelper({**data, "pathGambar": file.filename if file else ""})
    validator.required("nama", "Nama tidak boleh kosong")
    validator.required("deskripsi", "Deskripsi tidak boleh kosong")
    validator.required("manfaat", "Manfaat tidak boleh kosong")
    validator.required("efekSamping", "Efek Samping tidak boleh kosong")
    validator.required("pathGambar", "Gambar tidak boleh kosong")
    try:
        validator.validate()
    except ValueError as e:
        return fail("Data yang dikirimkan tidak valid!", str(e), 400)

    exist = plant_service.get_plant_by_name(data.get("nama"))
    if exist:
        return fail("Tumbuhan dengan nama ini sudah terdaftar!", status_code=409)

    try:
        new_id = plant_service.create_plant(data, file)
        return success("Berhasil menambahkan data tumbuhan", {"plantId": new_id}, 201)
    except Exception as e:
        return error(str(e))

@plant_bp.route("/plants/<id>", methods=["PUT", "OPTIONS"])
@cross_origin()
def update(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    plant = plant_service.get_plant_by_id(id)
    if not plant:
        return fail("Data tumbuhan tidak tersedia!", status_code=404)

    data = request.form.to_dict()
    file = request.files.get("gambar")

    try:
        updated = plant_service.update_plant(id, data, file)
        if not updated:
            return fail("Gagal memperbarui data tumbuhan!", status_code=400)
        return success("Berhasil mengubah data tumbuhan")
    except Exception as e:
        return error(str(e))

@plant_bp.route("/plants/<id>", methods=["DELETE", "OPTIONS"])
@cross_origin()
def delete(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    plant = plant_service.get_plant_by_id(id)
    if not plant:
        return fail("Data tumbuhan tidak tersedia!", status_code=404)

    try:
        deleted = plant_service.delete_plant(id)
        if not deleted:
            return fail("Gagal menghapus data tumbuhan!", status_code=400)
        return success("Berhasil menghapus data tumbuhan")
    except Exception as e:
        return error(str(e))

@plant_bp.route("/plants/<id>/image", methods=["GET"])
@cross_origin()
def get_image(id):
    plant = plant_service.get_plant_by_id(id)
    if not plant:
        return fail("Data tidak tersedia!", status_code=404)
    path = plant["pathGambar"]
    if not os.path.exists(path):
        return fail("Gambar tidak tersedia!", status_code=404)
    return send_file(path)