from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__, static_folder='.')
CORS(app)

analyzer = SentimentIntensityAnalyzer()

STATE = {
    "current_index": 0,
    "all_comments": [],
    "is_running": False
}

def load_data():
    try:
        with open("tiktok_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("data", {}).get("comments", []) or data.get("comments", [])
    except FileNotFoundError:
        return []

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')

@app.route('/scan', methods=['POST'])
def scan_route():
    payload = request.json
    keywords = [k.lower() for k in payload.get('keywords', [])]
    action = payload.get('action', 'refresh') 
    
    if action == 'start':
        STATE["all_comments"] = load_data()
        STATE["current_index"] = 0
        STATE["is_running"] = True
        return jsonify({"status": "started", "message": "Scan initialized."})

    if not STATE["is_running"]:
        return jsonify({"error": "Scan session not active"}), 400

    batch_size = 5 
    start = STATE["current_index"]
    end = start + batch_size
    
    batch = STATE["all_comments"][start:end]
    STATE["current_index"] += len(batch)

    stats = {kw: 0 for kw in keywords}
    matches = []

    for comment in batch:
        text = comment.get('text', '')
        text_lower = text.lower()
        
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        found_keywords = [kw for kw in keywords if kw in text_lower]
        
        if found_keywords:
            matches.append({
                "user": comment.get('username', 'Anonymous'),
                "text": text,
                "matches": found_keywords,
                "sentiment": sentiment 
            })
            for kw in found_keywords:
                stats[kw] += 1

    return jsonify({
        "status": "success",
        "new_comments_count": len(batch),
        "total_scanned_so_far": STATE["current_index"],
        "batch_stats": stats,
        "recent_matches": matches,
        "has_more": STATE["current_index"] < len(STATE["all_comments"])
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)