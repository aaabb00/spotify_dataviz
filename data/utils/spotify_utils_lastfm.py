# utils/spotify_utils_lastfm.py

from .spotify_utils import get_api_request, SPOTIFY_BASE_URL


def get_similar_track_data(token, track_name, artist_name):
    """
    For a 'similar track' from Last.fm, search first result on Spotify.
    Returns track_id, track_name, artist_name, spotify_url, is_playable.
    """
    if not track_name or not artist_name:
        return {}

    q = f"{track_name} {artist_name}"
    url = f"{SPOTIFY_BASE_URL}/search"
    data = get_api_request(token, url, params={"q": q, "type": "track", "limit": 1})
    if not data:
        return {}

    items = data.get("tracks", {}).get("items", [])
    if not items:
        return {}

    first_item = items[0]
    track_id = first_item.get("id")
    track_nm = first_item.get("name", track_name)
    playable = first_item.get("is_playable", True)
    ex_urls = first_item.get("external_urls", {})
    sp_url = ex_urls.get("spotify")

    # The first artist if present
    art_list = first_item.get("artists", [])
    main_artist_name = artist_name
    if art_list:
        main_artist_name = art_list[0].get("name", artist_name)

    out_data = {
        "track_id": track_id,
        "track_name": track_nm,
        "artist_name": main_artist_name,
        "track_spotify_url": sp_url,
        "is_playable": playable
    }
    return out_data


def search_artist_in_spotify(token, artist_name):
    """
    For a "similar artist" from Last.fm, Spotify search (type=artist, limit=1).
    Return { artist_name, artist_spotify_url, artist_image_url } or {} if none found.
    """
    if not artist_name:
        return {}

    data = get_api_request(token, f"{SPOTIFY_BASE_URL}/search",
                           params={"q": artist_name, "type": "artist", "limit": 1})
    if not data:
        return {}

    items = data.get("artists", {}).get("items", [])
    if not items:
        return {}

    first_item = items[0]
    external_urls = first_item.get("external_urls", {})
    images = first_item.get("images", [])

    out_info = {
        "name": first_item.get("name", artist_name),
        "artist_spotify_url": external_urls.get("spotify"),
        "artist_image_url": images[0]["url"] if images else None
    }
    return out_info