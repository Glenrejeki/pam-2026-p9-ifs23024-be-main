from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
from app.services import space_object_service
from app.utils.response import success, fail, error
from app.utils.validator import ValidatorHelper
import os

space_object_bp = Blueprint("space_object", __name__)

@space_object_bp.route("/space-objects", methods=["GET", "OPTIONS"])
@cross_origin()
def get_all():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    search = request.args.get("search", "")
    tipe = request.args.get("tipe", "")
    data = space_object_service.get_all_space_objects(search, tipe)
    return success("Berhasil mengambil daftar objek luar angkasa", {"spaceObjects": data})

@space_object_bp.route("/space-objects/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def get_by_id(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    obj = space_object_service.get_space_object_by_id(id)
    if not obj:
        return fail("Data objek luar angkasa tidak tersedia!", status_code=404)
    return success("Berhasil mengambil data objek luar angkasa", {"spaceObject": obj})

@space_object_bp.route("/space-objects", methods=["POST", "OPTIONS"])
@cross_origin()
def create():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.form.to_dict()
    file = request.files.get("gambar")

    validator = ValidatorHelper({**data, "pathGambar": file.filename if file else ""})
    validator.required("nama", "Nama tidak boleh kosong")
    validator.required("tipe", "Tipe tidak boleh kosong")
    validator.required("deskripsi", "Deskripsi tidak boleh kosong")
    validator.required("jarakDariBumi", "Jarak dari bumi tidak boleh kosong")
    validator.required("fakta", "Fakta tidak boleh kosong")
    validator.required("pathGambar", "Gambar tidak boleh kosong")
    try:
        validator.validate()
    except ValueError as e:
        return fail("Data yang dikirimkan tidak valid!", str(e), 400)

    exist = space_object_service.get_space_object_by_name(data.get("nama"))
    if exist:
        return fail("Objek dengan nama ini sudah terdaftar!", status_code=409)

    try:
        new_id = space_object_service.create_space_object(data, file)
        return success("Berhasil menambahkan data objek luar angkasa", {"spaceObjectId": new_id}, 201)
    except Exception as e:
        return error(str(e))

@space_object_bp.route("/space-objects/<id>", methods=["PUT", "OPTIONS"])
@cross_origin()
def update(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    obj = space_object_service.get_space_object_by_id(id)
    if not obj:
        return fail("Data objek luar angkasa tidak tersedia!", status_code=404)

    data = request.form.to_dict()
    file = request.files.get("gambar")

    try:
        updated = space_object_service.update_space_object(id, data, file)
        if not updated:
            return fail("Gagal memperbarui data objek luar angkasa!", status_code=400)
        return success("Berhasil mengubah data objek luar angkasa")
    except Exception as e:
        return error(str(e))

@space_object_bp.route("/space-objects/<id>", methods=["DELETE", "OPTIONS"])
@cross_origin()
def delete(id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    obj = space_object_service.get_space_object_by_id(id)
    if not obj:
        return fail("Data objek luar angkasa tidak tersedia!", status_code=404)

    try:
        deleted = space_object_service.delete_space_object(id)
        if not deleted:
            return fail("Gagal menghapus data objek luar angkasa!", status_code=400)
        return success("Berhasil menghapus data objek luar angkasa")
    except Exception as e:
        return error(str(e))

@space_object_bp.route("/space-objects/<id>/image", methods=["GET"])
@cross_origin()
def get_image(id):
    obj = space_object_service.get_space_object_by_id(id)
    if not obj:
        return fail("Data tidak tersedia!", status_code=404)
    path = obj["pathGambar"]
    if not os.path.exists(path):
        return fail("Gambar tidak tersedia!", status_code=404)
    return send_file(path)