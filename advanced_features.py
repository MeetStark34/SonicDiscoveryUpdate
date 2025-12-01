import random

class AdvancedFeatureEngine:
    def __init__(self, spotify_client):
        self.client = spotify_client

    # 🔮 1. Vibe Teleporter
    def vibe_teleporter(self, location, weather, time_of_day):
        """
        Generates params and SEED GENRES based on context.
        """
        params = {}
        seed_genres = []

        # Location Priors - Mapped to VALID Spotify Genres
        loc_map = {
            "Tokyo": ["j-pop", "j-rock", "anime"], 
            "London": ["british", "indie-pop", "house"], 
            "Paris": ["french", "electro", "chanson"], 
            "NYC": ["hip-hop", "jazz", "punk"], 
            "Rio": ["bossa-nova", "samba", "mpb"], 
            "Berlin": ["techno", "minimal-techno", "industrial"],
            "Mumbai": ["indian", "world-music"], 
        }
        if location in loc_map:
            seed_genres.extend(loc_map[location][:2])

        # Weather -> Audio Features
        if weather == "Rain":
            params['target_acousticness'] = 0.8
            params['target_energy'] = 0.3
            params['target_valence'] = 0.3
        elif weather == "Sunny":
            params['target_valence'] = 0.9
            params['target_energy'] = 0.8
        elif weather == "Snow":
            params['target_acousticness'] = 0.9
            params['target_energy'] = 0.2
            params['min_instrumentalness'] = 0.5

        # Time -> Energy/Tempo
        if time_of_day == "Night":
            params['target_danceability'] = 0.7
            params['min_popularity'] = 50
        elif time_of_day == "Morning":
            params['target_energy'] = 0.6
            params['target_valence'] = 0.7
        elif time_of_day == "Late Night":
            params['target_energy'] = 0.2
            params['target_tempo'] = 80

        return params, seed_genres

    # 🎨 8. Aesthetic Generator
    def aesthetic_generator(self, aesthetic):
        """
        Maps aesthetic names to musical attributes and SEED GENRES.
        """
        presets = {
            "Vaporwave": {"target_tempo": 90, "target_danceability": 0.6, "seed_genres": ["synth-pop", "funk"]},
            "Dark Academia": {"target_acousticness": 0.8, "target_instrumentalness": 0.7, "seed_genres": ["classical", "piano"]},
            "Cyberpunk": {"target_energy": 0.9, "target_distortion": 0.8, "target_tempo": 140, "seed_genres": ["industrial", "techno"]},
            "Cottagecore": {"target_acousticness": 0.9, "target_valence": 0.6, "seed_genres": ["folk", "acoustic", "country"]},
            "Neo-Noir": {"target_valence": 0.2, "target_tempo": 70, "seed_genres": ["jazz", "trip-hop"]}
        }
        data = presets.get(aesthetic, {})
        seed_genres = data.pop('seed_genres', [])
        return data, seed_genres

    # 🪞 4. Alternate You
    def alternate_you(self, top_genres):
        """
        Recommends opposite of user's taste using SEED GENRES.
        """
        # List of distinct genres to pick from if they are NOT in top_genres
        all_genres = ["classical", "metal", "country", "jazz", "techno", "reggae", "k-pop", "opera", "blues", "dubstep"]
        
        # Find genres the user DOESN'T listen to
        user_genres_str = " ".join([g[0] for g in top_genres]).lower()
        anti_genres = [g for g in all_genres if g not in user_genres_str]
        
        if not anti_genres:
            anti_genres = all_genres # Fallback
            
        # Pick 2 random anti-genres
        seed_genres = random.sample(anti_genres, min(2, len(anti_genres)))
        
        params = {
            'target_popularity': 20, # Discover hidden gems
            'target_energy': random.random()
        }
        return params, seed_genres
