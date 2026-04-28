from dotenv import load_dotenv
load_dotenv()  # ← harus SEBELUM import create_app

from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)