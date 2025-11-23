import json
import os
import random
import requests

from pathlib import Path
from flask import Flask, jsonify, render_template, send_from_directory

BASE_DIR = Path(__file__).parent
FACTS_FILE = BASE_DIR / "facts.json"

USE_API = os.getenv("Use API", "true").lower() in ["1", "true", "yes"]
API_URL = os.getenv("FACTS_API_URL", "https://uselessfacts.jsph.pl/random.json?language=en")

app = Flask(__name__)

def load_local_facts():
    if not FACTS_FILE.exists():
        return []
    with open(FACTS_FILE, 'r') as f:
        return json.load(f)
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/random-fact")
def random_fact():
    if USE_API:
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            text = data.get('text') or data.get("fact") or str(data)
            return jsonify({"source": "api", "fact": text})

        except Exception as e:
            local = load_local_facts()
            if local:
                return jsonify({"source": "local-fallback", "fact": random.choice(local)})
            return jsonify({"error": "failed to fetch fact", "details": {str(e)}}), 500
    
    local = load_local_facts()
    if not local:
        return jsonify({"error": "No local facts available"}), 500
    return jsonify({"source": "local", "fact": random.choice(local)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

