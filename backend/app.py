from flask import Flask, jsonify, send_from_directory
import requests
import random
import os

app = Flask(__name__)

@app.route("/quote")
def get_quote():
    # 1. Haal alle hoofdstukken van The Way (book_id=12)
    chapters_url = "https://escriva.org/api/v1/chapters?book_id=12&lang=en"
    chapters_resp = requests.get(chapters_url)
    if chapters_resp.status_code != 200:
        return jsonify({"quote": "Failed to fetch chapters"})
    chapters = chapters_resp.json()["results"]

    # 2. Kies random hoofdstuk
    chapter = random.choice(chapters)
    chapter_id = chapter["id"]

    # 3. Haal alle paragrafen (points) van dat hoofdstuk
    points_url = f"https://escriva.org/api/v1/points?chapter_id={chapter_id}&lang=en"
    points_resp = requests.get(points_url)
    if points_resp.status_code != 200:
        return jsonify({"quote": "Failed to fetch points"})
    points = points_resp.json()["results"]

    if not points:
        return jsonify({"quote": "No quotes found"})

    # 4. Kies random paragraaf
    random_point = random.choice(points)
    return jsonify({"quote": random_point.get("text", "No quote found.")})

@app.route("/")
def home():
    # Serve frontend
    return send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
