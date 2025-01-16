# utils/spotify_utils.py

import requests

SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

# ------------------------------------------------------------------------
# AUTH + API REQUEST
# ------------------------------------------------------------------------
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_api_request(token, url, params=None):
    """
    A generic GET request to Spotify Web API.
    """
    headers = get_auth_header(token)
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
    return None


# ------------------------------------------------------------------------
# SEARCH ORIGINAL RELEASES FOR REMASTER SONGS (decade mismatch)
# ------------------------------------------------------------------------
def words_overlap(query_str, found_str, min_common=2):
    """
    Returns True if 'query_str' and 'found_str' share at least 'min_common' words
    in lowercase form. Simple partial matching approach.
    """
    query_tokens = set(query_str.lower().split())
    found_tokens = set(found_str.lower().split())
    common = query_tokens & found_tokens
    if len(query_tokens) == 1:
        return len(common) == 1
    return len(common) >= min_common

def search_spotify_tracks_original_release(token, track_name, artist_name, decade, limit=10):
    """
    1) Build a Spotify query with year range from decade[:4] to decade[:4]+14.
    2) Parse up to 'limit' track results, pick the earliest 'album.release_date'.
    3) Check partial token-based overlap for both artist_name & track_name.
    4) Return {"found_item": best_item} or {} if none found.
    """
    try:
        start_decade = int(decade[:4])
    except:
        start_decade = 2020  # fallback

    query_str = f"{track_name} {artist_name}"
    url = f"{SPOTIFY_BASE_URL}/search"
    data = get_api_request(token, url, params={"q": query_str, "type": "track", "limit": limit})
    if not data:
        data = {}

    items = data.get("tracks", {}).get("items", [])
    if not items:
        return {}

    earliest_year = None
    best_item = None

    for itm in items:
        found_track_name = itm.get("name", "")
        if not words_overlap(track_name, found_track_name, min_common=1):
            continue

        art_list = itm.get("artists", [])
        if not art_list:
            continue
        found_artist_name = art_list[0].get("name", "")
        if not words_overlap(artist_name, found_artist_name, min_common=1):
            continue

        alb = itm.get("album", {})
        date_str = alb.get("release_date", "")
        if not date_str:
            continue

        year_str = date_str[:4]
        if not earliest_year or year_str < earliest_year:
            earliest_year = year_str
            best_item = itm

    if not best_item or not earliest_year:
        return {}
    return {"found_item": best_item}


# ------------------------------------------------------------------------
# ARTIST'S TOP TRACKS
# ------------------------------------------------------------------------
def get_artist_top_tracks(token, artist_id, market="US", limit=5):
    """
    Return a list of up to 'limit' top tracks for this artist in the given market.
    Each item includes minimal info { track_id, track_name, spotify_url, is_playable, album{...} }
    """
    url = f"{SPOTIFY_BASE_URL}/artists/{artist_id}/top-tracks"
    data = get_api_request(token, url, params={"market": market})
    if not data:
        return []

    top_tracks_list = []
    if data and "tracks" in data:
        for t_obj in data["tracks"][:limit]:
            tr_id = t_obj.get("id")
            tr_name = t_obj.get("name", "")
            playable = t_obj.get("is_playable", True)
            ext_urls = t_obj.get("external_urls", {})
            sp_url = ext_urls.get("spotify", None)

            alb_obj = t_obj.get("album", {})
            alb_imgs = alb_obj.get("images", [])
            alb_img_url = alb_imgs[0]["url"] if alb_imgs else None
            alb_release = alb_obj.get("release_date", "")
            alb_year = alb_release[:4] if alb_release else ""

            top_tracks_list.append({
                "track_id": tr_id,
                "track_name": tr_name,
                "is_playable": playable,
                "spotify_url": sp_url,
                "album": {
                    "id": alb_obj.get("id"),
                    "name": alb_obj.get("name"),
                    "image_url": alb_img_url,
                    "release_year": alb_year
                }
            })
    return top_tracks_list
