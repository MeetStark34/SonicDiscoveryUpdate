import streamlit as st
from auth import SpotifyAuthenticator
from spotify_client import SpotifyClient
import base64

# Page Config
st.set_page_config(
    page_title="SonicDiscovery", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Global Reset & Theme */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 10% 20%, rgba(29, 185, 84, 0.1) 0%, transparent 20%),
                          radial-gradient(circle at 90% 80%, rgba(29, 185, 84, 0.05) 0%, transparent 20%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1a1a1a;
    }
    
    /* Headers */
    h1 {
        font-weight: 800;
        background: linear-gradient(90deg, #1DB954, #1ED760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    h2, h3 { font-weight: 600; color: #fff; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #1DB954, #1aa34a);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
        width: 100%;
        text-transform: uppercase;
        font-size: 14px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.5);
    }
    
    /* Track Card (Grid Item) */
    .track-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .track-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        border-color: rgba(29, 185, 84, 0.3);
    }
    
    /* Image Container */
    .img-container {
        position: relative;
        width: 100%;
        padding-top: 100%; /* 1:1 Aspect Ratio */
        border-radius: 12px;
        overflow: hidden;
        background: #121212;
    }
    .img-container img {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .track-card:hover img { transform: scale(1.05); }
    
    /* Typography */
    .track-title {
        font-weight: 600;
        font-size: 15px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 5px;
    }
    .track-artist {
        font-size: 13px;
        color: #b3b3b3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Action Button */
    .play-btn {
        margin-top: auto;
        background: rgba(255,255,255,0.1);
        color: #1DB954;
        text-align: center;
        padding: 8px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none;
        transition: background 0.2s;
        display: block;
    }
    .play-btn:hover { background: rgba(255,255,255,0.2); }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #555; }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] { margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

from advanced_features import AdvancedFeatureEngine

def main():
    try:
        authenticator = SpotifyAuthenticator()
    except ValueError as e:
        st.error(f"Config Error: {e}")
        return

    if "code" in st.query_params:
        try:
            token = authenticator.get_token_from_code(st.query_params["code"])
            st.session_state["token"] = token
            st.query_params.clear()
            st.rerun()
        except Exception:
            st.error("Auth failed")

    if "token" not in st.session_state:
        cached = authenticator.get_cached_token()
        if cached: st.session_state["token"] = cached

    if "token" not in st.session_state:
        show_login(authenticator)
    else:
        try:
            sp = authenticator.get_spotify_client(st.session_state["token"])
            client = SpotifyClient(sp)
            engine = AdvancedFeatureEngine(client)
            show_app(client, engine)

        except Exception as e:
            st.error(f"Session Expired or Error: {e}")
            st.session_state.pop("token", None)
            import os
            if os.path.exists(".spotify_cache"):
                try:
                    os.remove(".spotify_cache")
                except:
                    pass
            st.button("Login Again", on_click=lambda: st.rerun())

def show_login(auth):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 3rem; margin-bottom: 10px;">SonicDiscovery</h1>
            <p style="color: #b3b3b3; font-size: 1.2rem;">Your Personal AI Music Curator</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("CONNECT SPOTIFY", auth.get_auth_url(), use_container_width=True)

def show_app(client, engine):
    user = client.get_user_profile()
    
    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; padding: 20px 0; border-bottom: 1px solid #222; margin-bottom: 20px;">
            <img src="{user['images'][0]['url'] if user['images'] else 'https://via.placeholder.com/50'}" 
                 style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid #1DB954;">
            <div style="font-weight: 600;">{user['display_name']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        menu_options = [
            "Dashboard", "Discover", "Mood Tuner", "Time Travel",
            "🔮 Vibe Teleporter", "🎨 Aesthetic Gen", "🪞 Alternate You"
        ]
        page = st.radio("MENU", menu_options, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.pop("token", None)
            import os
            if os.path.exists(".spotify_cache"): os.remove(".spotify_cache")
            st.rerun()

    if page == "Dashboard":
        st.title("Dashboard")
        
        # 1. Top Eras / Genres
        st.subheader("Your Taste Profile")
        genres = client.get_top_genres()
        cols = st.columns(5)
        for i, (g, c) in enumerate(genres[:5]):
            with cols[i]:
                st.markdown(f"""
                <div style="background: #181818; border: 1px solid #333; padding: 15px; border-radius: 12px; text-align: center;">
                    <div style="color: #1DB954; font-weight: 800; font-size: 20px;">#{i+1}</div>
                    <div style="font-size: 14px; text-transform: capitalize;">{g}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Top Artists
        st.subheader("Your Top Artists")
        top_artists = client.get_top_artists(5)
        if top_artists:
            cols = st.columns(5)
            for i, artist in enumerate(top_artists):
                with cols[i]:
                    img_url = artist['image_url'] if artist['image_url'] else "https://via.placeholder.com/150"
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <img src="{img_url}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 2px solid #333;">
                        <div style="margin-top: 10px; font-weight: 600; font-size: 14px;">{artist['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No top artists found yet.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Top Tracks
        st.subheader("Your Top Tracks")
        render_track_grid(client.get_top_tracks(4))

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. New Releases
        st.subheader("New Releases")
        new_releases = client.get_new_releases(4)
        if new_releases:
            cols = st.columns(4)
            for i, album in enumerate(new_releases):
                with cols[i % 4]:
                     img_url = album['image_url'] if album['image_url'] else "https://via.placeholder.com/300"
                     st.markdown(f"""
                     <div class="track-card">
                        <div class="img-container">
                            <img src="{img_url}">
                        </div>
                        <div class="track-title" title="{album['name']}">{album['name']}</div>
                        <div class="track-artist" title="{', '.join(album['artists'])}">{', '.join(album['artists'])}</div>
                        <div style="font_size: 12px; color: #888; margin-top: 5px;">{album['release_date']}</div>
                        <a href="{album['external_url']}" target="_blank" class="play-btn">OPEN SPOTIFY</a>
                     </div>
                     """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 5. Recently Liked
        st.subheader("Recently Liked")
        render_track_grid(client.get_liked_tracks(8))

    elif page == "Discover":
        st.title("Discover New Music")
        if st.button("GENERATE"):
            with st.spinner("Analyzing..."):
                seeds = [t['id'] for t in client.get_liked_tracks(50)]
                if seeds:
                    recs = client.get_recommendations(seeds, limit=12)
                    render_track_grid(recs)

    elif page == "Mood Tuner":
        st.title("Mood Tuner")
        col1, col2 = st.columns(2)
        with col1: val = st.slider("Sad <-> Happy", 0.0, 1.0, 0.5)
        with col2: en = st.slider("Chill <-> Hype", 0.0, 1.0, 0.5)
        if st.button("TUNE IN"):
            seeds = [t['id'] for t in client.get_liked_tracks(50)]
            recs = client.get_recommendations(seeds, target_valence=val, target_energy=en, limit=12)
            render_track_grid(recs)

    elif page == "Time Travel":
        st.title("Time Travel")
        decade = st.select_slider("Select Era", [1960, 1970, 1980, 1990, 2000, 2010])
        if st.button(f"WARP TO {decade}s"):
            recs = client.search_decade(decade, decade+9, limit=12)
            render_track_grid(recs)

    # --- NEW ADVANCED FEATURES ---

    elif page == "🔮 Vibe Teleporter":
        st.title("🔮 Vibe Teleporter")
        st.markdown("Generate a playlist based on a specific time and place.")
        c1, c2, c3 = st.columns(3)
        with c1: loc = st.selectbox("Location", ["Tokyo", "London", "Paris", "NYC", "Berlin", "Rio"])
        with c2: weather = st.selectbox("Weather", ["Rain", "Sunny", "Snow", "Cloudy"])
        with c3: time = st.selectbox("Time", ["Morning", "Night", "Late Night"])
        
        if st.button("TELEPORT"):
            params, seed_genres = engine.vibe_teleporter(loc, weather, time)
            # Pass seed_genres explicitly, do NOT pass seed_tracks
            recs = client.get_recommendations(seed_genres=seed_genres, limit=12, **params)
            render_track_grid(recs)

    elif page == "🎨 Aesthetic Gen":
        st.title("🎨 Aesthetic Generator")
        aes = st.selectbox("Choose Aesthetic", ["Vaporwave", "Dark Academia", "Cyberpunk", "Cottagecore", "Neo-Noir"])
        if st.button("GENERATE"):
            params, seed_genres = engine.aesthetic_generator(aes)
            # Filter out non-API params like 'genres' if any remain (already popped in engine)
            recs = client.get_recommendations(seed_genres=seed_genres, limit=12, **params)
            render_track_grid(recs)

    elif page == "🪞 Alternate You":
        st.title("🪞 Alternate You")
        st.markdown("Meet the version of you from a parallel universe.")
        if st.button("SIMULATE ALTERNATE SELF"):
            # Pass top genres to find opposites
            top_genres = client.get_top_genres()
            params, seed_genres = engine.alternate_you(top_genres)
            recs = client.get_recommendations(seed_genres=seed_genres, limit=12, **params)
            render_track_grid(recs)

def render_track_grid(tracks):
    if not tracks:
        st.info("No tracks found.")
        return

    # Create a 4-column grid
    cols = st.columns(4)
    for i, t in enumerate(tracks):
        col = cols[i % 4]
        with col:
            img_url = t['image_url'] if t['image_url'] else "https://via.placeholder.com/300"
            
            # Use flat string for HTML to avoid indentation issues
            html = f"""
<div class="track-card">
    <div class="img-container">
        <img src="{img_url}">
    </div>
    <div class="track-title" title="{t['name']}">{t['name']}</div>
    <div class="track-artist" title="{', '.join(t['artists'])}">{', '.join(t['artists'])}</div>
    <a href="{t['external_url']}" target="_blank" class="play-btn">OPEN IN SPOTIFY</a>
</div>
"""
            st.markdown(html, unsafe_allow_html=True)
            
            # Optional: Add native audio player below card if preview exists
            if t['preview_url']:
                st.audio(t['preview_url'], format='audio/mp3')

if __name__ == "__main__":
    main()
