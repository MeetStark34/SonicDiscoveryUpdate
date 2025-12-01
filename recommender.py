import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from feature_extraction import FeatureExtractor

class RecommenderSystem:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.scaler = StandardScaler()

    def prepare_data(self, tracks, spotify_client):
        """
        Extracts features for a list of tracks.
        Returns a DataFrame of features and a list of track info.
        """
        track_ids = [t['id'] for t in tracks]
        audio_features_list = spotify_client.get_audio_features(track_ids)
        
        feature_vectors = []
        valid_tracks = []
        
        for track, audio_feat in zip(tracks, audio_features_list):
            # If audio_feat is None (due to API failure), use empty dict to generate zero vector
            feat_input = audio_feat if audio_feat else {}
            vector = self.feature_extractor.process_track(track, feat_input)
            feature_vectors.append(vector)
            valid_tracks.append(track)
        
        if not feature_vectors:
            return pd.DataFrame(), []

        X = np.array(feature_vectors)
        return X, valid_tracks

    def recommend(self, source_tracks, candidate_tracks, spotify_client, top_n=10):
        """
        Recommends tracks from candidate_tracks based on similarity to source_tracks.
        """
        # 1. Prepare Source Data (User Profile)
        X_source, _ = self.prepare_data(source_tracks, spotify_client)
        
        # 2. Prepare Candidate Data
        X_candidates, valid_candidates = self.prepare_data(candidate_tracks, spotify_client)
        
        # If we have no candidates, return empty
        if not valid_candidates:
            return []

        # If feature extraction failed (all zeros), we fallback to random or simple ranking
        # Check if X_source is empty or all zeros
        if len(X_source) == 0 or np.all(X_source == 0):
            # Just return the candidates as is (they are already "recommendations" from Spotify/Artist top tracks)
            return [{'track': t, 'score': 0.0} for t in valid_candidates][:top_n]

        # 3. Normalize
        # Fit scaler on both to ensure consistent scaling
        try:
            X_combined = np.vstack([X_source, X_candidates])
            self.scaler.fit(X_combined)
            
            X_source_scaled = self.scaler.transform(X_source)
            X_candidates_scaled = self.scaler.transform(X_candidates)

            # 4. Create User Profile Vector (Mean of source tracks)
            user_profile = np.mean(X_source_scaled, axis=0).reshape(1, -1)

            # 5. Compute Cosine Similarity
            similarities = cosine_similarity(user_profile, X_candidates_scaled)[0]
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            # Fallback: return candidates with 0 score
            return [{'track': t, 'score': 0.0} for t in valid_candidates][:top_n]

        # 6. Rank Candidates
        recommendations = []
        for i, score in enumerate(similarities):
            recommendations.append({
                'track': valid_candidates[i],
                'score': float(score)
            })
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Filter out tracks that might be in source_tracks (by ID)
        source_ids = set(t['id'] for t in source_tracks)
        final_recs = [r for r in recommendations if r['track']['id'] not in source_ids]
        
        # Ensure we return something even if all filtered (unlikely)
        if not final_recs:
             final_recs = recommendations
        
        return final_recs[:top_n]
