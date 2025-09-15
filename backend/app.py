from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/quote")
def get_quote():
    url = "https://www.escriva.org/en/quote-of-the-day"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Let op: de class kan verschillen afhankelijk van de site
    quote_element = soup.find("div", class_="quote")
    quote = quote_element.get_text(strip=True) if quote_element else "No quote found."

    return jsonify({"quote": quote})

if __name__ == "__main__":
    app.run(debug=True)
