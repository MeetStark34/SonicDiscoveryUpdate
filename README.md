# 🎵 SonicDiscovery

**Your Personal AI Music Curator.**

SonicDiscovery is a next-generation music recommendation engine that goes beyond simple "similar songs." It connects to your Spotify account to offer immersive, context-aware, and aesthetic-based music discovery experiences.

**✨ New Architecture:**
- **Frontend**: React (Vite) + TailwindCSS + Framer Motion (Premium Glassmorphism UI)
- **Backend**: FastAPI (Python) + Spotipy

> **Note**: The original Streamlit implementation has been moved to the `legacy-streamlit` branch.

## ✨ Features

### 🚀 Core Experience
- **Dashboard**: Interactive stats, "Audio DNA" visualization, and "Your #1s" highlights.
- **Discover**: Generate personalized recommendations based on your listening history (Top Artists + Top Tracks model).
- **Mood Tuner**: Fine-tune your recommendations with "Sad <-> Happy" and "Chill <-> Hype" sliders.
- **Time Travel**: Warp to specific decades (60s, 70s, 80s, 90s, 00s, 10s) and explore the hits of that era.

### 🔮 Advanced AI Features
- **Vibe Teleporter**: Generate playlists for specific contexts (e.g., "Tokyo + Rain + Night").
- **Aesthetic Generator**: Curate music based on internet aesthetics like *Vaporwave*, *Dark Academia*, and *Cyberpunk*.
- **Alternate You**: Meet your musical doppelgänger from a parallel universe.

## 📦 Installation

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- A Spotify Developer Account

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sonic-discovery.git
   cd sonic-discovery
   ```

2. **Backend Setup** (in `server/` directory)
   ```bash
   cd server
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Environment Configuration**:
   Create a `.env` file in the project root (not `server/`):
   ```ini
   SPOTIPY_CLIENT_ID='your_client_id'
   SPOTIPY_CLIENT_SECRET='your_client_secret'
   SPOTIPY_REDIRECT_URI='http://127.0.0.1:8501/callback'
   ```

3. **Frontend Setup** (in `client/` directory)
   ```bash
   cd ../client
   npm install
   ```

## 🚀 Running the App

You need to run both the backend and frontend terminals.

**Terminal 1 (Backend):**
```bash
cd server
python -m uvicorn main:app --port 8501 --reload
```

**Terminal 2 (Frontend):**
```bash
cd client
npm run dev
```

Open **http://localhost:5173** to start discovering!
