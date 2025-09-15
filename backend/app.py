from flask import Flask, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

@app.route("/quote")
def get_quote():
    url = "https://escriva.org/en/book/the-way/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    paragraphs = soup.find_all("p")  # later scherper maken met juiste class
    if not paragraphs:
        return jsonify({"quote": "No quotes found on escriva.org"})

    random_paragraph = random.choice(paragraphs).get_text(strip=True)
    return jsonify({"quote": random_paragraph})

@app.route("/")
def home():
    # dit zoekt in de map ../frontend naar index.html
    return send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
