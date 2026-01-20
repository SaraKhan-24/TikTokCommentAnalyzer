# TikTok Trend & Sentiment Scanner

> **Real-time keyword analytics, trend velocity tracking, and AI-powered sentiment analysis for TikTok comments.**

![Project Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
[![Python](https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=python)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/Frontend-Chart.js-yellow?style=for-the-badge&logo=javascript)](https://www.chartjs.org/)
[![AI](https://img.shields.io/badge/AI-VADER%20Sentiment-orange?style=for-the-badge)](https://github.com/cjhutto/vaderSentiment)

## About The Project

This application allows marketers, dropshippers, and content creators to analyze the comment section of viral TikTok videos in real-time. Instead of manually reading thousands of comments, this tool visualizes **Trend Velocity**, **Keyword Distribution**, and **Audience Sentiment**.

It solves the "Data Overload" problem by answering:
* *"Is the audience buying this product or calling it a scam?"*
* *"Which specific product shade or feature is going viral?"*
* *"Is the sentiment actually positive, or just sarcastic?"* (Powered by VADER)

### Key Features
* **"Credit-Safe" Architecture:** Fetches data once and simulates real-time streams to save expensive API credits during development and analysis.
* **AI Sentiment Engine:** Uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to correctly interpret social media context, including emojis (😍 vs 😡), slang, and capitalization.
* **Live Trend Velocity:** Visualizes spikes in keyword mentions to detect viral moments as they happen.
* **Instant Feedback Loop:** A decoupled Flask backend feeds data batches to a reactive JavaScript frontend.

---

## Dashboard Screenshots

| **Dashboard Overview** | **Trend Velocity Graph** |
|:---:|:---:|
| ![Dashboard Overview](./image_54c5fb.png) | ![Trend Graph](./image_17a357.png) |
| *Real-time stats & Sentiment Feed* | *Keyword mentions over time* |

| **Sentiment Analysis in Action** |
|:---:|
| ![Sentiment Feed](./image_5a80aa.png) |
| *VADER correctly identifying emoji sentiment* |

---

## Tech Stack

* **Backend:** Python 3, Flask (REST API)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
* **Visualization:** Chart.js
* **Data Science:** `vaderSentiment` (NLP)
* **Data Source:** SocialKit API
* **Data Storage:** Local JSON (Simulating NoSQL Database)

---

## Getting Started

### Prerequisites
* Python 3.8+
* A [SocialKit](https://socialkit.io/) API Key (for fetching new data)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/tiktok-scanner.git](https://github.com/yourusername/tiktok-scanner.git)
cd tiktok-scanner

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Ensure `vaderSentiment`, `flask`, `flask-cors`, `requests`, and `python-dotenv` are in your requirements.txt)*

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your API key:

```ini
SOCIALKIT_API_KEY=your_api_key_here

```

---

## How to Use

### Phase 1: Data Collection (The Fetcher)

To save API credits, we fetch the comments **once** and save them locally.
Run the fetch script:

```bash
python fetcher.py

```

* **Input:** The URL of the TikTok video you want to analyze.
* **Output:** A `tiktok_data.json` file containing raw comment data.
* *Note: This step requires internet access and valid API credits.*

### Phase 2: Live Analysis (The Server)

Launch the Flask server to process the data and serve the dashboard:

```bash
python server.py

```

* You will see: `⚡ TikTok Scanner Server Running on http://localhost:5000`

### Phase 3: The Dashboard

1. Open your browser and go to `http://localhost:5000`.
2. **Configuration:**
* Enter the TikTok URL (for reference).
* Enter Keywords to track (comma-separated).
* *Example:* `shade, love, price, buy, sold out, hope, wonder`


3. Click **"Start Scan"** to initialize the data stream.
4. Click **"Fetch New"** to simulate incoming real-time comment batches.
5. Watch the **Trend Velocity** chart spike and the **Sentiment Feed** update with emoji-aware tags!

---

## Architecture Overview

This project uses a **Decoupled Client-Server Architecture**:

1. **The Fetcher:** Python script handles the external API connection, pagination, rate limits, and data cleaning.
2. **The Bridge:** `tiktok_data.json` acts as a data buffer, allowing for unlimited replayability of analysis without incurring API costs.
3. **The Server:** Flask reads the JSON, performs **Sentiment Analysis** on the fly using VADER, and serves "batches" of data to the frontend.
4. **The Client:** JavaScript receives the analyzed batches and updates the DOM and Charts instantly without page reloads.

---

## Future Improvements

* [ ] **Automated Interval:** Add a toggle to auto-click "Fetch New" every 3 seconds.
* [ ] **Export Data:** Add a "Download CSV" button for Excel integration.
* [ ] **Multi-Video Compare:** Compare sentiment across two different videos simultaneously.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/yourusername/tiktok-scanner/issues).

## License

This project is [MIT](https://www.google.com/search?q=LICENSE) licensed.

```

```