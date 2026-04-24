from app.config import Config

def get_profile():
    return {
        "username": "abdullah.ubaid",
        "nama": "Abdullah Ubaid",
        "tentang": "Saya adalah seorang developer yang tertarik pada mobile development, backend API, dan berbagai teknologi pengembangan aplikasi.",
        "photo": f"{Config.BASE_URL}/static/profile/me.png",
    }