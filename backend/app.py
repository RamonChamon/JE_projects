from flask import Flask, jsonify
import requests
import random
import os

app = Flask(__name__)

@app.route("/quote")
def get_quote():
    # 1. Alle hoofdstukken ophalen
    chapters_url = "https://escriva.org/api/v1/books/camino/chapters?lang=en"
    chapters_resp = requests.get(chapters_url)
    chapters = chapters_resp.json()

    # Kies random hoofdstuk
    chapter = random.choice(chapters)
    chapter_id = chapter["id"]

    # 2. Paragrafen uit dit hoofdstuk halen
    chapter_url = f"https://escriva.org/api/v1/books/camino/chapters/{chapter_id}?lang=en"
    chapter_resp = requests.get(chapter_url)
    chapter_data = chapter_resp.json()

    # 3. Kies random paragraaf (text veld)
    paragraphs = chapter_data.get("paragraphs", [])
    if not paragraphs:
        return jsonify({"quote": "No paragraphs found."})

    random_paragraph = random.choice(paragraphs).get("text", "No quote found.")
    return jsonify({"quote": random_paragraph})

@app.route("/")
def home():
    return app.send_static_file("../frontend/index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
