# 🎵 SonicDiscovery

**Your Personal AI Music Curator.**

SonicDiscovery is a next-generation music recommendation engine that goes beyond simple "similar songs." It connects to your Spotify account to offer immersive, context-aware, and aesthetic-based music discovery experiences.

## ✨ Features

### 🚀 Core Experience
- **Dashboard**: Visualize your top genres and recently liked tracks in a premium grid layout.
- **Discover**: Generate personalized recommendations based on your listening history.
- **Mood Tuner**: Fine-tune your recommendations with "Sad <-> Happy" and "Chill <-> Hype" sliders.
- **Time Travel**: Warp to specific decades (60s, 70s, 80s, 90s, 00s, 10s) and explore the hits of that era.

### 🔮 Advanced AI Features
- **Vibe Teleporter**: Generate playlists for specific contexts (e.g., "Tokyo + Rain + Night" or "Rio + Sunny + Morning").
- **Aesthetic Generator**: Curate music based on internet aesthetics like *Vaporwave*, *Dark Academia*, *Cyberpunk*, and *Cottagecore*.
- **Alternate You**: Meet your musical doppelgänger from a parallel universe (recommends genres you *don't* usually listen to).

### 🛠️ Technical Highlights
- **Robust "Search-Based" Engine**: A fail-safe recommendation system that uses smart search queries to guarantee results even if Spotify's recommendation API fails.
- **Premium UI**: A sleek, dark-mode interface built with Streamlit and custom CSS, featuring glassmorphism, hover effects, and responsive grids.
- **Secure Auth**: OAuth 2.0 integration for secure Spotify login.

## 📦 Installation

### Prerequisites
- Python 3.10+
- A Spotify Developer Account

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sonic-discovery.git
   cd sonic-discovery
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Create a `.env` file in the project root.
   - Add your Spotify credentials:
     ```ini
     SPOTIPY_CLIENT_ID='your_client_id'
     SPOTIPY_CLIENT_SECRET='your_client_secret'
     SPOTIPY_REDIRECT_URI='http://localhost:8501/callback'
     ```

4. **Run the App**
   ```bash
   python main.py
   ```

## 📝 License
MIT
