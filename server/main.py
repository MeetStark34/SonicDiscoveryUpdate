from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

import os
import sys

# Add current directory to path to find adjacent modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import SpotifyAuthenticator
from spotify_client import SpotifyClient
from advanced_features import AdvancedFeatureEngine
import spotipy

app = FastAPI(title="SonicDiscovery API")

origins = [
    "https://sonic-discovery-update-pi.vercel.app",  # Your actual Vercel URL
    "http://localhost:5173",  # Keep for local development
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    code: str

# --- Dependencies ---
def get_authenticator():
    try:
        return SpotifyAuthenticator()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_client(request: Request, auth: SpotifyAuthenticator = Depends(get_authenticator)):
    token = request.cookies.get("spotify_token")
    if not token:
        # Check header just in case
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
         raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        sp = spotipy.Spotify(auth=token)
        return SpotifyClient(sp)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Auth Routes ---

@app.get("/login")
def login(auth: SpotifyAuthenticator = Depends(get_authenticator)):
    return RedirectResponse(url=auth.get_auth_url())

@app.get("/callback")
def callback(code: str, auth: SpotifyAuthenticator = Depends(get_authenticator)):
    try:
        token_info = auth.get_token_from_code(code)
        access_token = token_info['access_token']
        
        # Redirect to Frontend Dashboard (matching domain)
        response = RedirectResponse(url=f"https://sonic-discovery-update-pi.vercel.app/dashboard?token={access_token}")
        
        # Set HttpOnly cookie for production (HTTPS with cross-domain support)
        response.set_cookie(
            key="spotify_token", 
            value=access_token, 
            httponly=True, 
            samesite="none",  # Required for cross-domain cookies (Vercel frontend + Render backend)
            secure=True,      # Required for HTTPS in production
            path="/"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Auth failed: {str(e)}")

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("spotify_token")
    return {"status": "logged_out"}

@app.get("/me")
def get_profile(client: SpotifyClient = Depends(get_client)):
    return client.get_user_profile()

# --- Dashboard Routes ---

@app.get("/dashboard/stats")
def get_dashboard_stats(client: SpotifyClient = Depends(get_client)):
    return {
        "top_genres": client.get_top_genres(5),
        "top_artists": client.get_top_artists(5),
        "top_tracks": client.get_top_tracks(4),
        "new_releases": client.get_new_releases(4),
        "recent": client.get_liked_tracks(8),
        "audio_profile": client.get_audio_profile(),
        "listening_stats": client.get_listening_stats()
    }

@app.get("/dashboard/audio-profile")
def get_audio_profile(client: SpotifyClient = Depends(get_client)):
    """Returns user's audio profile based on their top tracks."""
    profile = client.get_audio_profile()
    if not profile:
        raise HTTPException(status_code=404, detail="Could not generate audio profile")
    return profile

@app.get("/dashboard/listening-stats")
def get_listening_stats(client: SpotifyClient = Depends(get_client)):
    """Returns comprehensive listening statistics."""
    return client.get_listening_stats()

# --- Feature Routes ---

@app.get("/features/discover")
def discover(client: SpotifyClient = Depends(get_client)):
    """
    Improved discovery using mixed seeds from:
    - Top tracks (listening history)
    - Top artists
    - Liked tracks (fallback)
    """
    seeds = client.get_mixed_seeds()
    
    # Build recommendation request with available seeds
    kwargs = {'limit': 12}
    if seeds['seed_tracks']:
        kwargs['seed_tracks'] = seeds['seed_tracks']
    if seeds['seed_artists']:
        kwargs['seed_artists'] = seeds['seed_artists']
    
    # If we have no seeds at all, use genre fallback
    if not seeds['seed_tracks'] and not seeds['seed_artists']:
        return client.get_recommendations(seed_genres=['pop', 'rock'], limit=12)
    
    return client.get_recommendations(**kwargs)

@app.get("/features/mood")
def mood_tuner(valence: float, energy: float, client: SpotifyClient = Depends(get_client)):
    """
    Mood-based recommendations using mixed seeds.
    """
    seeds = client.get_mixed_seeds()
    
    kwargs = {
        'limit': 12,
        'target_valence': valence,
        'target_energy': energy
    }
    
    if seeds['seed_tracks']:
        kwargs['seed_tracks'] = seeds['seed_tracks']
    if seeds['seed_artists']:
        kwargs['seed_artists'] = seeds['seed_artists']
    
    if not seeds['seed_tracks'] and not seeds['seed_artists']:
        kwargs['seed_genres'] = ['pop']
    
    return client.get_recommendations(**kwargs)

@app.get("/features/time-travel")
def time_travel(year: int, client: SpotifyClient = Depends(get_client)):
    return client.search_decade(year, year+9, limit=12)

@app.get("/features/vibe")
def vibe_teleporter(location: str, weather: str, time: str, client: SpotifyClient = Depends(get_client)):
    engine = AdvancedFeatureEngine(client)
    params, seed_genres = engine.vibe_teleporter(location, weather, time)
    return client.get_recommendations(seed_genres=seed_genres, limit=12, **params)

@app.get("/features/aesthetic")
def aesthetic(style: str, client: SpotifyClient = Depends(get_client)):
    engine = AdvancedFeatureEngine(client)
    params, seed_genres = engine.aesthetic_generator(style)
    return client.get_recommendations(seed_genres=seed_genres, limit=12, **params)

@app.get("/features/alternate")
def alternate_you(client: SpotifyClient = Depends(get_client)):
    engine = AdvancedFeatureEngine(client)
    top_genres = client.get_top_genres()
    params, seed_genres = engine.alternate_you(top_genres)
    return client.get_recommendations(seed_genres=seed_genres, limit=12, **params)

# Run with: uvicorn main:app --reload