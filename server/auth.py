import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load .env from project root (parent of server/)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)


class SpotifyAuthenticator:
    """
    Handles Spotify Authentication using Authorization Code Flow
    with PER-SESSION token cache.
    """

    def __init__(self, cache_path: str):
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
            cache_path=cache_path,   # ✅ PER-SESSION CACHE
            show_dialog=True
        )

    def get_auth_url(self, state: str):
        """Generates the Spotify login URL with state."""
        return self.sp_oauth.get_authorize_url(state=state)

    def get_token_from_code(self, code: str):
        """Exchanges auth code for access token."""
        return self.sp_oauth.get_access_token(code, as_dict=True)

    def get_cached_token(self):
        """Retrieves cached token if valid."""
        return self.sp_oauth.get_cached_token()

    def get_spotify_client(self, token_info):
        """Returns a spotipy client instance."""
        return spotipy.Spotify(auth=token_info["access_token"])
