# utils/dataframes_spotify.py

import pandas as pd
from .spotify_utils import (
    get_api_request,
    get_artist_top_tracks,
    search_spotify_tracks_original_release
)
from .spotify_utils_batch import get_several_tracks, get_several_artists

SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

# A dictionary-of-sets approach for sub-genre -> main genre
GENRE_SETS = {
    "hip-hop": {"hip-hop", "hip hop", "rap"},
    "rock": {"rock", "punk", "metal", "hard rock"},
    "pop": {"pop", "dance pop", "electropop"},
    "soul": {"soul", "funk", "r&b"},
    "alternative": {"alternative", "indie", "indie rock"},
    "electronic": {"electronic", "edm", "techno", "house"},
    "jazz": {"jazz", "blues"},
    "country": {"country"},
}


def map_main_genre(artist_genres):
    """
    Return the first matching main genre from GENRE_SETS, else 'other'.
    """
    for g in artist_genres:
        g_low = g.lower()
        for main_genre, synonyms in GENRE_SETS.items():
            for syn in synonyms:
                syn_low = syn.lower()
                if g_low == syn_low or syn_low in g_low:
                    return main_genre
    return "other"


def build_track_df(token, tracks, track_ids, is_from_playlist=False, decade=None):
    """
    Returns a tracks dataframe.
    If album_year doesn't match the decade prefix (except "2020s"),
    calls `search_spotify_track() to find an earlier date
    and updates the album fields accordingly.
    """
    # Gather track IDs
    track_dict = get_several_tracks(token, track_ids)

    artist_ids_set = set()
    for t_id, t_obj in track_dict.items():
        for art_ref in t_obj.get("artists", []):
            artist_ids_set.add(art_ref["id"])
    artist_dict = get_several_artists(token, list(artist_ids_set))

    rows = []

    for rank, t_item in enumerate(tracks):
        t_id = t_item.get("track", "").get("id", "") if is_from_playlist else t_item.get("id", "")
        if t_id not in track_dict:
            print(f"t_id {t_id} not in tract_dict")
            continue

        full_tr = track_dict[t_id]

        # Basic track / playlist fields
        d = dict()

        d["track_rank"] = rank
        d["track_id"] = t_id
        d["track_name"] = full_tr.get("name")
        # parse integer popularity
        d["track_popularity"] = int(full_tr.get("popularity", 0))
        d["duration_ms"] = full_tr.get("duration_ms")
        d["explicit"] = full_tr.get("explicit", False)
        d["is_playable"] = t_item.get("is_playable", True)

        # track spotify url
        tr_ext = full_tr.get("external_urls", {})
        d["track_spotify_url"] = tr_ext.get("spotify")

        # album details
        alb = full_tr.get("album", {})
        d["album_id"] = alb.get("id")
        d["album_name"] = alb.get("name", "")
        alb_date = alb.get("release_date", "")
        d["album_year"] = alb_date[:4] if alb_date else ""
        alb_imgs = alb.get("images", [])
        d["album_image_url"] = alb_imgs[0]["url"] if alb_imgs else None
        alb_ext = alb.get("external_urls", {})
        d["album_spotify_url"] = alb_ext.get("spotify", None)

        if d["album_year"]:
            d["real_decade_prefix"] = d["album_year"][:3]
            d["real_decade"] = d["real_decade_prefix"] + "0s"
        else:
            d["real_decade"] = ""
            d["real_decade_prefix"] = ""


        # parse main + feat artists
        arts_list = full_tr.get("artists", [])
        d["artist_id"] = None
        d["artist_name"] = None
        d["artist_followers"] = None
        d["artist_popularity"] = None
        d["feat_artists"] = []
        d["main_genre"] = "other"

        if arts_list:
            # main
            main_a = arts_list[0]
            a_id = main_a.get("id", "")
            main_a_obj = artist_dict.get(a_id, {})
            d["artist_id"] = a_id
            d["artist_name"] = main_a.get("name", "")
            d["artist_followers"] = main_a_obj.get("followers", {}).get("total", 0)
            d["artist_popularity"] = main_a_obj.get("popularity", 0)
            d["artist_name"] = main_a_obj.get("name", main_a.get("name"))
            # sub-genres -> main_genre
            sub_gs = main_a_obj.get("genres", [])
            d["main_genre"] = map_main_genre(sub_gs)

            # gather feat
            if len(arts_list) > 1:
                for feat_art in arts_list[1:]:
                    d["feat_artists"].append({
                        "id": feat_art.get("id", ""),
                        "name": feat_art.get("name", "")
                    })

        # mismatch => search older track (if not "2020s" decade)
        from_decade = decade if decade else d["real_decade"]
        start_decade = int(from_decade[:4])
        alb_year_int = int(d["album_year"]) if d["album_year"] else 0
        if (alb_year_int < start_decade - 5) or (alb_year_int > start_decade + 12):
            from_name = d["track_name"] or ""
            from_artist = d["artist_name"] or ""
            re_search = search_spotify_tracks_original_release(token, from_name, from_artist, from_decade)
            if re_search and "found_item" in re_search:
                best_item = re_search["found_item"]
                new_alb = best_item.get("album", {})
                new_date = new_alb.get("release_date", "")
                d["album_id"] = new_alb.get("id")
                d["album_name"] = new_alb.get("name", "")
                d["album_year"] = new_date[:4] if new_date else ""
                new_alb_imgs = new_alb.get("images", [])
                d["album_image_url"] = new_alb_imgs[0]["url"] if new_alb_imgs else None
                new_alb_ext = new_alb.get("external_urls", {})
                d["album_spotify_url"] = new_alb_ext.get("spotify", None)

                # re-check real_decade after new album_year
                if d["album_year"]:
                    d["real_decade_prefix"] = d["album_year"][:3]
                    d["real_decade"] = d["real_decade_prefix"] + "0s"
                else:
                    d["real_decade"] = ""
                    d["real_decade_prefix"] = ""

        rows.append(d)

    final_cols = [
        "track_rank", "track_id", "track_name", "track_popularity", "duration_ms",
        "explicit", "is_playable", "track_spotify_url",
        "album_id", "album_name", "album_year", "album_image_url", "album_spotify_url",
        "real_decade", "real_decade_prefix",
        "artist_id", "artist_name", "artist_followers", "artist_popularity", "feat_artists",
        "main_genre"
    ]
    df_tracks = pd.DataFrame(rows, columns=final_cols)
    return df_tracks



def build_playlist_tracks_df(token, playlist_id, decade="Now", limit=50):
    """
    1) Fetch playlist's top tracks from /playlists/{playlist_id}
    2) build_tracks_df(...) => dataframes of tracks
    3) Concat playlist_df (id, name, url, decade) + track_df -> Return Dataframe
    """
    # 1) fetch the playlist JSON
    url = f"{SPOTIFY_BASE_URL}/playlists/{playlist_id}"
    playlist_json = get_api_request(token, url)
    if not playlist_json:
        print(f"No playlist data for {playlist_id}")
        return pd.DataFrame()

    # Create playlist-level df
    playlist_df = pd.DataFrame(columns=["playlist_id", "playlist_name", "playlist_spotify_url", "decade"])

    # Get Tracks till limit
    tracks = playlist_json["tracks"].get("items", [])[:limit]
    track_ids = []
    for t_item in tracks:
        t_id = t_item.get("track", "").get("id", "")
        if t_id:
            track_ids.append(t_id)

    # Parse track into dataframe
    track_df = build_track_df(token, tracks, track_ids, is_from_playlist=True)

    # Concat both dataframes
    df_tracks = pd.concat([playlist_df, track_df], axis=1)
    df_tracks["playlist_id"] = playlist_id
    df_tracks["playlist_name"] = playlist_json.get("name", "")
    df_tracks["playlist_spotify_url"] = playlist_json.get("external_urls", {}).get("spotify", None)
    df_tracks["decade"] = decade
    print(f"Number of tracks saved from playlist: {len(df_tracks)}")
    return df_tracks



def build_spotify_artists_df(token, df_tracks):
    """
    Gathers unique artist_id (including feat artists) from df_tracks, fetch from Spotify,
    adds "artist_spotify_url", "artist_image_url", "artist_genres", etc.
    Also adds a new column "artist_top_tracks" for top 5 tracks of each artist.
    """

    if df_tracks.empty:
        return pd.DataFrame()

    # 1) Collect main artist IDs
    main_artist_ids = df_tracks["artist_id"].dropna().unique().tolist()

    # 2) Collect feat artist IDs
    feat_ids = []
    feat_ids = []
    for feat_list in df_tracks["feat_artists"]:
        # feat_list might be an empty list or a list of dicts
        if isinstance(feat_list, list):
            for feat_art_dict in feat_list:
                feat_id = feat_art_dict.get("id", "")
                if feat_id:
                    feat_ids.append(feat_id)

    all_artist_ids = list(set(main_artist_ids + feat_ids))
    if not all_artist_ids:
        return pd.DataFrame()

    # 3) Request artist objects
    artist_dict = get_several_artists(token, all_artist_ids)

    # 4) Build rows for "artist_top_tracks" column
    rows = []
    for a_id in all_artist_ids:
        a_obj = artist_dict.get(a_id)
        if not a_obj:
            continue

        name = a_obj.get("name", "")
        popularity = int(a_obj.get("popularity", 0))
        followers = int(a_obj.get("followers", {}).get("total", 0))
        genres = a_obj.get("genres", [])
        images = a_obj.get("images", [])
        image_url = images[0]["url"] if images else None
        ext_urls = a_obj.get("external_urls", {})
        artist_sp_url = ext_urls.get("spotify", None)

        # Get top 5 tracks for this artist
        top_tracks_list = get_artist_top_tracks(token, a_id, limit=5)

        row = {
            "artist_id": a_id,
            "artist_name": name,
            "artist_popularity": popularity,
            "artist_followers": followers,
            "artist_genres": genres,
            "artist_image_url": image_url,
            "artist_spotify_url": artist_sp_url,
            "artist_top_tracks": top_tracks_list
        }
        rows.append(row)

    columns = [
        "artist_id", "artist_name", "artist_popularity",
        "artist_followers", "artist_genres", "artist_image_url",
        "artist_spotify_url", "artist_top_tracks"
    ]
    df_artists = pd.DataFrame(rows, columns=columns)
    return df_artists
