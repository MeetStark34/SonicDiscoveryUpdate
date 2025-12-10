import spotipy
from spotipy.exceptions import SpotifyException
import random

class SpotifyClient:
    def __init__(self, sp):
        self.sp = sp
        # Hardcoded safe genres to avoid slow API call on startup
        self.valid_genres = {
            'acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 
            'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 
            'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 
            'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 
            'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 
            'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 
            'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 
            'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 
            'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 
            'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 
            'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 
            'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 
            'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 
            'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 
            'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 
            'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 
            'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 
            'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 
            'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 
            'world-music'
        }

    def get_user_profile(self):
        return self.sp.current_user()

    def get_liked_tracks(self, limit=20):
        try:
            results = self.sp.current_user_saved_tracks(limit=limit)
            return [self._format_track(item['track']) for item in results['items']]
        except Exception:
            return []

    def get_user_playlists(self):
        try:
            results = self.sp.current_user_playlists(limit=20)
            return [{'id': i['id'], 'name': i['name']} for i in results['items']]
        except Exception:
            return []

    def get_top_genres(self, limit=10):
        try:
            results = self.sp.current_user_top_artists(limit=20, time_range='medium_term')
            genres = {}
            for artist in results['items']:
                for genre in artist['genres']:
                    genres[genre] = genres.get(genre, 0) + 1
            return sorted(genres.items(), key=lambda x: x[1], reverse=True)[:limit]
        except Exception:
            return []

    def get_top_artists(self, limit=10):
        try:
            results = self.sp.current_user_top_artists(limit=limit, time_range='medium_term')
            return [{'name': i['name'], 'image_url': i['images'][0]['url'] if i['images'] else None, 'external_url': i['external_urls']['spotify']} for i in results['items']]
        except Exception:
            return []

    def get_top_tracks(self, limit=10):
        try:
            results = self.sp.current_user_top_tracks(limit=limit, time_range='medium_term')
            return [self._format_track(item) for item in results['items']]
        except Exception:
            return []

    def get_new_releases(self, limit=10):
        try:
            results = self.sp.new_releases(limit=limit, country='US')
            # New releases are albums, so we need to format differently or pick first track? 
            # Actually, standard format requires 'track' structure. 
            # API returns albums. Let's return simplified album objects or adapt.
            # To keep it simple and compatible with simple image/text display, I'll return a custom object list
            # but ideally I should adhere to _format_track if possible.
            # However, albums don't have 'preview_url' in the same way. 
            # Let's return a list of dicts similar to artists but for albums.
            return [{
                'name': i['name'], 
                'artists': [a['name'] for a in i['artists']],
                'image_url': i['images'][0]['url'] if i['images'] else None, 
                'external_url': i['external_urls']['spotify'],
                'release_date': i['release_date']
            } for i in results['albums']['items']]
        except Exception:
            return []

    def get_recommendations(self, seed_tracks=None, seed_genres=None, seed_artists=None, limit=10, **kwargs):
        """
        Robust recommendation fetcher. Tries standard API, falls back to Search/TopTracks.
        """
        seeds = {}
        if seed_tracks: seeds['seed_tracks'] = seed_tracks[:5]
        elif seed_genres: seeds['seed_genres'] = seed_genres[:5]
        elif seed_artists: seeds['seed_artists'] = seed_artists[:5]
        else: seeds['seed_genres'] = ['pop']

        # Attempt 1: Standard API (might 404)
        try:
            results = self.sp.recommendations(limit=limit, **seeds, **kwargs)
            if results['tracks']: return [self._format_track(t) for t in results['tracks']]
        except Exception as e:
            print(f"Standard Rec API failed: {e}")

        # Attempt 2: Search-Based Fallback (The "Manual" Way)
        print("Switching to Search-Based Recommendation Engine...")
        return self._recommend_via_search(seed_genres, seed_artists, seed_tracks, limit)

    def _recommend_via_search(self, genres, artists, tracks, limit):
        """
        Manually constructs a playlist using Search and Artist Top Tracks.
        """
        recs = []
        try:
            # Strategy A: Genre Search
            if genres:
                for g in genres:
                    # Search for tracks in this genre with a random offset for variety
                    offset = random.randint(0, 50)
                    q = f"genre:{g}"
                    results = self.sp.search(q=q, type='track', limit=20, offset=offset)
                    for t in results['tracks']['items']:
                        recs.append(self._format_track(t))
            
            # Strategy B: Artist Top Tracks (ID or Name)
            if artists:
                for a_seed in artists:
                    try:
                        # Check if it's a name-based seed (from Sonic Multiverse)
                        if a_seed.startswith("name:"):
                            artist_name = a_seed.replace("name:", "")
                            print(f"Searching for artist: {artist_name}")
                            
                            # Try 1: Specific Artist Search
                            q = f"artist:{artist_name}"
                            results = self.sp.search(q=q, type='track', limit=10)
                            if results['tracks']['items']:
                                for t in results['tracks']['items']:
                                    recs.append(self._format_track(t))
                            else:
                                # Try 2: General Search (Brute Force)
                                print(f"Specific search failed, trying general: {artist_name}")
                                results = self.sp.search(q=artist_name, type='track', limit=10)
                                for t in results['tracks']['items']:
                                    recs.append(self._format_track(t))

                        else:
                            # It's an ID (standard fallback)
                            top = self.sp.artist_top_tracks(a_seed, country='US')
                            if top['tracks']:
                                for t in top['tracks']:
                                    recs.append(self._format_track(t))
                            else:
                                # Fallback: Search by Name if ID fails
                                artist_info = self.sp.artist(a_seed)
                                q = f"artist:{artist_info['name']}"
                                results = self.sp.search(q=q, type='track', limit=10)
                                for t in results['tracks']['items']:
                                    recs.append(self._format_track(t))
                    except Exception as e:
                        print(f"Artist search error for {a_seed}: {e}")
                        pass

            # Strategy C: Tracks -> Artists -> Top Tracks
            if tracks:
                # Fetch full track info to get artist IDs
                try:
                    full_tracks = self.sp.tracks(tracks[:5])
                    artist_ids = set()
                    for t in full_tracks['tracks']:
                        if t and t['artists']:
                            artist_ids.add(t['artists'][0]['id'])
                    
                    for a_id in list(artist_ids)[:3]:
                        try:
                            top = self.sp.artist_top_tracks(a_id, country='US')
                            for t in top['tracks']:
                                recs.append(self._format_track(t))
                        except:
                            pass
                except:
                    pass

            # If still empty, Ultimate Fallback: Search "Pop"
            if not recs:
                results = self.sp.search(q="genre:pop", type='track', limit=20)
                for t in results['tracks']['items']:
                    recs.append(self._format_track(t))

            # Shuffle and return unique tracks
            random.shuffle(recs)
            # Deduplicate by ID
            unique_recs = []
            seen_ids = set()
            for r in recs:
                if r['id'] not in seen_ids:
                    unique_recs.append(r)
                    seen_ids.add(r['id'])
            
            return unique_recs[:limit]

        except Exception as e:
            print(f"Search Fallback failed: {e}")
            return []

    def search_decade(self, start_year, end_year, limit=10):
        query = f"year:{start_year}-{end_year}"
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            return [self._format_track(t) for t in results['tracks']['items']]
        except Exception:
            return []

    def _format_track(self, track):
        return {
            'id': track['id'],
            'name': track['name'],
            'artists': [a['name'] for a in track['artists']],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'uri': track['uri']
        }
