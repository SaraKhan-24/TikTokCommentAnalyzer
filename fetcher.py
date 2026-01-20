from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__, static_folder='.')
CORS(app)

analyzer = SentimentIntensityAnalyzer()

STATE = {
    "index": 0,
    "data": [],
    "active": False
}

def get_local_data():
    try:
        with open("tiktok_data.json", "r", encoding="utf-8") as f:
            content = json.load(f)
            return content.get("data", {}).get("comments", []) or content.get("comments", [])
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/app.js')
def static_js():
    return send_from_directory('.', 'app.js')

@app.route('/scan', methods=['POST'])
def process_scan():
    req_data = request.json
    keywords = [k.lower() for k in req_data.get('keywords', [])]
    action = req_data.get('action', 'refresh') 
    
    if action == 'start':
        STATE["data"] = get_local_data()
        STATE["index"] = 0
        STATE["active"] = True
        return jsonify({"status": "initialized"})

    if not STATE["active"]:
        return jsonify({"error": "Session not started"}), 400

    batch_size = 5 
    start = STATE["index"]
    end = start + batch_size
    
    subset = STATE["data"][start:end]
    STATE["index"] += len(subset)

    stats = {k: 0 for k in keywords}
    matches = []

    for item in subset:
        raw_text = item.get('text', '')
        text_lower = raw_text.lower()
        
        sentiment_score = analyzer.polarity_scores(raw_text)['compound']
        
        if sentiment_score >= 0.05:
            label = "Positive"
        elif sentiment_score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        hits = [k for k in keywords if k in text_lower]
        
        if hits:
            matches.append({
                "user": item.get('username', 'User'),
                "text": raw_text,
                "keywords": hits,
                "sentiment": label 
            })
            for k in hits:
                stats[k] += 1

    return jsonify({
        "count": len(subset),
        "total": STATE["index"],
        "stats": stats,
        "results": matches,
        "more": STATE["index"] < len(STATE["data"])
    })

if __name__ == '__main__':
    app.run(port=5000)