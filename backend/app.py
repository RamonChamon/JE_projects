from flask import Flask, jsonify, send_from_directory
import requests
import random
import os
from bs4 import BeautifulSoup  # to clean up HTML

app = Flask(__name__)

@app.route("/quote")
def get_quote():
    # 1. Get all chapters from The Way (book_id=12)
    chapters_url = "https://escriva.org/api/v1/chapters?book_id=12&lang=en"
    chapters_resp = requests.get(chapters_url)
    if chapters_resp.status_code != 200:
        return jsonify({"quote": "Failed to fetch chapters"})
    chapters = chapters_resp.json()["results"]

    # 2. Pick a random chapter
    chapter = random.choice(chapters)
    chapter_id = chapter["id"]

    # 3. Get all points from that chapter
    points_url = f"https://escriva.org/api/v1/points?chapter_id={chapter_id}&lang=en"
    points_resp = requests.get(points_url)
    if points_resp.status_code != 200:
        return jsonify({"quote": "Failed to fetch points"})
    points = points_resp.json()["results"]

    if not points:
        return jsonify({"quote": "No quotes found"})

    # 4. Pick a random point
    random_point = random.choice(points)

    # Clean the HTML tags from the text
    quote_html = random_point.get("text", "No quote found.")
    quote_text = BeautifulSoup(quote_html, "html.parser").get_text(strip=True)

    # Get the point number ("order")
    quote_number = random_point.get("order", "?")

    return jsonify({
        "quote": quote_text,
        "number": quote_number,
        "book": "The Way"
    })

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
