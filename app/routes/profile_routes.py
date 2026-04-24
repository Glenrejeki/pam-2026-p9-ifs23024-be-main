from flask import Blueprint, jsonify, send_file, request
from flask_cors import cross_origin
from app.services.profile_service import get_profile
from app.utils.response import success, fail
import os

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET", "OPTIONS"])
@cross_origin()
def profile():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    return success("Berhasil mengambil profile pengembang", get_profile())

@profile_bp.route("/profile/photo", methods=["GET"])
@cross_origin()
def profile_photo():
    path = "uploads/profile/me.png"
    if not os.path.exists(path):
        return fail("Foto tidak tersedia!", status_code=404)
    return send_file(path)