# utils/spotify_utils_batch.py

from .spotify_utils import get_api_request, SPOTIFY_BASE_URL


def chunk_list(lst, chunk_size=50):

    for i in range(0, len(lst), chunk_size):
        yield lst[i : i+chunk_size]


def get_several_tracks(token, track_ids):
    """
    Batch request  using chunk_list() of up to 50 track IDs from /v1/tracks.
    Return {track_id: track_obj}.
    """
    track_info_dict = {}
    for chunk in chunk_list(track_ids, 50):
        ids_str = ",".join(chunk)
        url = f"{SPOTIFY_BASE_URL}/tracks"
        # use get_api_request instead of direct requests
        data = get_api_request(token, url, params={"ids": ids_str})
        if not data:
            continue

        # parse
        tracks_list = data.get("tracks", [])
        if tracks_list:
            for tr_obj in tracks_list:
                if tr_obj and "id" in tr_obj:
                    track_info_dict[tr_obj["id"]] = tr_obj
    return track_info_dict


def get_several_artists(token, artist_ids):
    """
    Batch request using chunk_list() of up to 50 artist IDs from /v1/artists.
    Return {artist_id: artist_obj}.
    """
    artist_info_dict = {}
    for chunk in chunk_list(artist_ids, 50):
        ids_str = ",".join(chunk)
        url = f"{SPOTIFY_BASE_URL}/artists"
        data = get_api_request(token, url, params={"ids": ids_str})
        if not data:
            continue

        # parse
        artists_list = data.get("artists", [])
        if artists_list:
            for art_obj in artists_list:
                if art_obj and "id" in art_obj:
                    artist_info_dict[art_obj["id"]] = art_obj
    return artist_info_dict
