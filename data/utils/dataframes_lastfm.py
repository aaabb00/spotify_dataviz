# utils/dataframes_lastfm.py

import pandas as pd
from .lastfm_utils import lastfm_get_similar_tracks, lastfm_get_similar_artists
from .spotify_utils_lastfm import get_similar_track_data, search_artist_in_spotify


def build_similar_tracks_df(token, lastfm_api_key, df_tracks, limit=5):
    """
    Build a DataFrame of similar tracks from Last.fm, then get data for each from Spotify search:
      1) Get unique artists from tracks and for each,
      2) Get up to 'limit' similar tracks from lastfm_get_similar_tracks
      3) Call get_similar_track_data() to find the best matching track on Spotify
      4) Store columns: original_track_id, track_id,  track_name, artist_name,
         is_playable, track_spotify_url
    """
    if df_tracks.empty or not lastfm_api_key:
        return pd.DataFrame()

    # Map unique artists from tracks: track_id -> (track_name, artist_name)
    track_map = {}
    for idx, row in df_tracks.iterrows():
        t_id = row["track_id"]
        tname = row.get("track_name")
        aname = row.get("artist_name")
        if t_id and tname and aname:
            track_map[t_id] = (tname, aname)

    sim_rows = []
    for orig_tid, (tname, aname) in track_map.items():
        # Last.fm similar
        similar_list = lastfm_get_similar_tracks(lastfm_api_key, tname, aname, limit=limit)
        for sim_obj in similar_list:
            s_tname = sim_obj["track_name"]
            s_aname = sim_obj["artist_name"]
            # Search in Spotify
            sim_data = get_similar_track_data(token, s_tname, s_aname)
            row_sim = {
                "original_track_id": orig_tid,
                "track_id": sim_data.get("track_id"),
                "track_name": sim_data.get("track_name", s_tname),
                "artist_name": sim_data.get("artist_name", s_aname),
                "is_playable": sim_data.get("is_playable", True),
                "track_spotify_url": sim_data.get("track_spotify_url")
            }
            sim_rows.append(row_sim)

    columns = [
        "original_track_id", "track_id",  "track_name", "artist_name",
        "is_playable", "track_spotify_url"
    ]
    return pd.DataFrame(sim_rows, columns=columns)


def build_similar_artists_df(token, lastfm_api_key, df_artists, limit=5):
    """
    Build a DataFrame of similar artists from Last.fm, then get data for each from Spotify search:
      1) For each artist in df_artists get up to 'limit' similar artists from lastfm_get_similar_artists
      2) Call search_artist_in_spotify() to find the best matching artist on Spotify
      3) Store columns: original_artist_id, artist_name, artist_spotify_url, artist_image_url
    """
    if df_artists.empty or not lastfm_api_key:
        return pd.DataFrame()

    sim_rows = []
    for idx, row in df_artists.iterrows():
        a_id = row["artist_id"]
        a_name = row["artist_name"]
        if not a_id or not a_name:
            continue
        # last.fm
        sim_names = lastfm_get_similar_artists(lastfm_api_key, a_name, limit=limit)
        for sim_n in sim_names:
            if not sim_n:
                continue
            # Search artist in Spotify (exact match)
            df_match = df_artists[df_artists["artist_name"].str.lower().isin([sim_n.lower()])]
            if df_match.empty:
                # Artist not in dataframe -> Search in Spotify
                sp_info = search_artist_in_spotify(token, sim_n)
            else:
                sp_info = df_match.iloc[0]
            row_sim = {
                "original_artist_id": a_id,
                "artist_name": sp_info.get("artist_name", sim_n),
                "artist_spotify_url": sp_info.get("artist_spotify_url"),
                "artist_image_url": sp_info.get("artist_image_url")
            }
            sim_rows.append(row_sim)

    cols = ["original_artist_id", "artist_name", "artist_spotify_url", "artist_image_url"]
    return pd.DataFrame(sim_rows, columns=cols)
