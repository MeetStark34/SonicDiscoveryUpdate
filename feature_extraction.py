import numpy as np
import requests
import os
import tempfile
import pandas as pd

# librosa is not supported on Python 3.14 yet, so we disable it.
# import librosa 

class FeatureExtractor:
    """
    Handles extraction of audio features from Spotify API.
    Raw audio analysis (Librosa) is currently disabled due to Python 3.14 incompatibility.
    """
    
    SPOTIFY_AUDIO_FEATURES = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]

    def __init__(self):
        pass

    def download_preview(self, preview_url):
        """Downloads the preview MP3 to a temporary file."""
        if not preview_url:
            return None
        
        try:
            response = requests.get(preview_url)
            if response.status_code == 200:
                fd, path = tempfile.mkstemp(suffix=".mp3")
                with os.fdopen(fd, 'wb') as tmp:
                    tmp.write(response.content)
                return path
        except Exception as e:
            print(f"Error downloading preview: {e}")
        return None

    def extract_librosa_features(self, file_path):
        """
        Mock function for Librosa features.
        Returns a zero vector since librosa is disabled.
        """
        # 13 MFCC + 1 Centroid + 1 Rolloff = 15 features
        return np.zeros(15)

    def process_track(self, track_info, audio_features):
        """
        Combines Spotify features and (Mock) Librosa features into a single vector.
        track_info: dict containing 'preview_url', 'id', 'name'
        audio_features: dict from Spotify API
        """
        # 1. Spotify Features
        spotify_vector = []
        if audio_features:
            for feature in self.SPOTIFY_AUDIO_FEATURES:
                spotify_vector.append(audio_features.get(feature, 0))
        else:
            spotify_vector = [0] * len(self.SPOTIFY_AUDIO_FEATURES)
            
        # 2. Librosa Features (Skipped)
        librosa_vector = np.zeros(15)
        
        # Combine
        full_vector = np.concatenate([spotify_vector, librosa_vector])
        return full_vector

    def get_feature_names(self):
        librosa_names = [f'mfcc_{i}' for i in range(13)] + ['spectral_centroid', 'spectral_rolloff']
        return self.SPOTIFY_AUDIO_FEATURES + librosa_names
