from flask import Blueprint, request, jsonify
from app.services.motivation_service import (
    create_motivations,
    get_all_motivations
)

motivation_bp = Blueprint("motivation", __name__)

@motivation_bp.route("/", methods=["GET"])
def index():
    return "API telah berjalan! Dibuat oleh Abdullah Ubaid"

# Tambahkan OPTIONS untuk handle preflight
@motivation_bp.route("/motivations/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json()
    theme = data.get("theme")
    total = data.get("total")

    if not theme:
        return jsonify({"error": "Theme is required"}), 400

    if not total:
        return jsonify({"error": "Total is required"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_motivations(theme, total)
        return jsonify({
            "theme": theme,
            "total": len(result),
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Tambahkan OPTIONS untuk handle preflight
@motivation_bp.route("/motivations", methods=["GET", "OPTIONS"])
def get_all():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    data = get_all_motivations(page=page, per_page=per_page)
    return jsonify(data)