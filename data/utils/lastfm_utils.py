# utils/lastfm_utils.py

import os
import requests
from dotenv import load_dotenv

LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0"

def get_lastfm_api_data():
    """
    Returns Last.fm API KEY from an .env file.
    """
    api_key = os.environ.get("LASTFM_API_KEY")
    if not api_key:
        print("No LASTFM_API_KEY found.")
        return None, None
    print("LASTFM_API_KEY found")
    return api_key


def lastfm_request(method, api_key, params):
    base_params = {
        "method": method,
        "api_key": api_key,
        "format": "json"
    }
    final_params = {**base_params, **params}
    try:
        r = requests.get(LASTFM_BASE_URL, params=final_params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Last.fm request error ({method}): {e}")
        return None
    except ValueError as e:
        print(f"Last.fm parse error ({method}): {e}")
        return None


def lastfm_get_similar_tracks(api_key, track_name, artist_name, limit=5):
    if not api_key or not track_name or not artist_name:
        return []
    data = lastfm_request("track.getSimilar", api_key, {
        "track": track_name,
        "artist": artist_name,
        "limit": limit
    })
    results = []
    if data and "similartracks" in data:
        items = data["similartracks"].get("track", [])
        for itm in items[:limit]:
            art = itm.get("artist", {})
            results.append({
                "track_name": itm.get("name"),
                "artist_name": art.get("name")
            })
    return results


def lastfm_get_similar_artists(api_key, artist_name, limit=5):
    if not api_key or not artist_name:
        return []
    data = lastfm_request("artist.getSimilar", api_key, {
        "artist": artist_name,
        "limit": limit
    })
    results = []
    if data and "similarartists" in data:
        items = data["similarartists"].get("artist", [])
        for itm in items[:limit]:
            results.append(itm.get("name", ""))
    return results
