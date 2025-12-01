import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class SpotifyAuthenticator:
    """
    Handles Spotify Authentication using Authorization Code Flow.
    """
    def __init__(self):
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        self.scope = "user-library-read playlist-read-private user-top-read"

        if not self.client_id or not self.client_secret or not self.redirect_uri:
            raise ValueError("Missing Spotify credentials in .env file")

        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".spotify_cache"
        )

    def get_auth_url(self):
        """Generates the Spotify login URL."""
        return self.sp_oauth.get_authorize_url()

    def get_token_from_code(self, code):
        """Exchanges auth code for access token."""
        return self.sp_oauth.get_access_token(code)

    def get_cached_token(self):
        """Retrieves cached token if valid."""
        token_info = self.sp_oauth.get_cached_token()
        if token_info:
            return token_info
        return None

    def get_spotify_client(self, token_info):
        """Returns a spotipy client instance."""
        return spotipy.Spotify(auth=token_info['access_token'])
