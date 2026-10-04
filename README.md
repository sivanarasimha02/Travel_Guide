# 🌍 AI Travel Guide

An AI-powered, multilingual travel companion that generates custom audio guides and rich destination overviews on demand using **Google Gemini AI** and **Murf AI**.

---

## 🌟 Features

- **🏰 Curated & Custom Destinations**: Explore famous landmarks (Taj Mahal, Red Fort, Gateway of India, Hawa Mahal, Golden Temple, Mysore Palace) or search for any global destination.
- **⏱️ Flexible Guide Lengths**:
  - **Summarized (~1 min)**: Concise overview highlighting historical and cultural significance.
  - **Detailed (~3 min)**: Immersive storytelling covering history, architecture, and visitor insights.
- **🗣️ Multi-Language Support**: English, Hindi, Tamil, and Telugu.
- **🎙️ Natural Voice Synthesis**: Choose between Male and Female voice actors powered by Murf AI low-latency streaming TTS.
- **📜 Read Along Transcript**: Interactive, collapsible transcript view synced with the audio guide.
- **⚡ Modern Responsive UI**: Built with Tailwind CSS, clean card animations, and responsive layout.
- **🛡️ Built-in Resilience**: Automatic fallback across Gemini models (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) during API capacity spikes.

---

## 📁 Project Structure

```text
TRAVEL GUIDE_FINAL_CODE/
├── Backend/
│   └── app.py            # Flask API server & static file host
├── Frontend/
│   ├── index.html        # Main web interface (Tailwind CSS)
│   └── index.js          # UI interactions & API integration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Google Gemini API Key** ([Get from Google AI Studio](https://aistudio.google.com/))
- **Murf AI API Key** ([Get from Murf.ai](https://murf.ai/))

---

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "TRAVEL GUIDE_FINAL_CODE"
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Configuration (Environment Variables)

Create a `.env` file in the root directory (or set environment variables):

```env
GEMINI_API_KEY="your_gemini_api_key_here"
MURF_API_KEY="your_murf_api_key_here"
PORT=5001
```

*(If `.env` is omitted, default API keys configured in `Backend/app.py` will be used.)*

---

### Running the Application

1. **Start the Flask backend server**:
   ```bash
   python Backend/app.py
   ```
   *(Or using virtual environment: `./.venv/bin/python Backend/app.py`)*

2. **Open the web application**:
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5001
   ```

---

## 🚢 Deployment: Vercel (Frontend) & Render (Backend)

### 1️⃣ Deploy Backend on Render

1. **Push your code to GitHub/GitLab**.
2. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** → **Web Service**.
3. Connect your repository.
4. Render automatically reads [render.yaml](render.yaml) and [Procfile](Procfile):
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 Backend.app:app`
5. Under **Environment Variables**, add:
   - `GEMINI_API_KEY` = your Google Gemini API key
   - `MURF_API_KEY` = your Murf AI API key
6. Click **Deploy**. Once live, copy your Render Web Service URL (e.g. `https://travel-guide-backend.onrender.com`).

---

### 2️⃣ Connect Frontend & Deploy on Vercel

1. In [Frontend/index.js](Frontend/index.js), update `RENDER_BACKEND_URL` on line 130 with your Render service URL:
   ```javascript
   const RENDER_BACKEND_URL = "https://your-backend.onrender.com";
   ```
2. **Deploy with Vercel**:
   - **Via CLI**:
     ```bash
     ./deploy.sh vercel
     ```
   - **Or via Vercel Dashboard**:
     1. Import your GitHub repository on [vercel.com/new](https://vercel.com/new).
     2. Keep root settings (Vercel automatically detects [vercel.json](vercel.json)).
     3. Click **Deploy**.

---

### 3️⃣ Local & Container Deployment

- **Local Dev Server**: `./deploy.sh dev` (runs on `http://127.0.0.1:5001`)
- **Local Prod (Gunicorn)**: `./deploy.sh prod`
- **Docker Compose**: `docker-compose up -d --build`

---

## 📡 API Reference

### `POST /generate-audio-guide`

Generates an AI description and synthesizes streaming speech audio for a given destination.

#### Request Body
```json
{
  "place": "Taj Mahal",
  "answerType": "Summary",
  "language": "English",
  "voiceId": "Matthew",
  "locale": "en-US"
}
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `place` | string | Destination name or landmark (Required) |
| `answerType` | string | `"Summary"` or `"Detailed"` (Default: `"Summary"`) |
| `language` | string | `"English"`, `"Hindi"`, `"Tamil"`, or `"Telugu"` |
| `voiceId` | string | Murf Voice ID (e.g., `"Matthew"`, `"Alicia"`, `"Aman"`) |
| `locale` | string | Target locale code (e.g., `"en-US"`, `"hi-IN"`, `"ta-IN"`, `"te-IN"`) |

#### Response
```json
{
  "description": "Welcome to the Taj Mahal...",
  "audioBase64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEA..."
}
```

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Tailwind CSS, JavaScript (ES6+), Web Audio API
- **Backend**: Python 3, Flask, Flask-CORS
- **AI & Speech Services**:
  - [Google GenAI SDK](https://github.com/google/generative-ai-python) (`gemini-2.5-flash`)
  - [Murf AI Streaming TTS API](https://murf.ai/api) (Falcon model)
