# data/main_general_data.py

import os
import pandas as pd
import datetime

from data.utils.spotify_auth import get_spotify_api_data, get_spotify_api_token
from data.utils.lastfm_utils import get_lastfm_api_data
from data.utils.dataframes_spotify import build_playlist_tracks_df, build_spotify_artists_df
from data.utils.dataframes_lastfm import build_similar_tracks_df, build_similar_artists_df
from data.analysis.tracks_csv_analysis import track_analysis, delete_mismatch_release_year


def export_csv_in_dir(df, csv_path, csv_name):
    """
    Export dataframe as CSV in csv_path.
    """
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    file_path = os.path.join(csv_path, csv_name)
    df.to_csv(file_path, index=False)
    print(f"Saved dataframe as CSV in {file_path}")


def main():
    # Load Spotify + Last.fm creds
    client_id, client_secret, redirect_uri = get_spotify_api_data()
    spotify_token = get_spotify_api_token(client_id, client_secret)

    lastfm_api_key = get_lastfm_api_data()

    if not spotify_token:
        print("No valid Spotify token. Exiting.")
        return

    # 7 playlists
    playlists_to_get = {
        "1960s": "4ZuX2YvKAlym0a8VozqV1U",
        "1970s": "5KmBulox9POMt9hOt3VV1x",
        "1980s": "70N5mgNl3QBQB09zXoa72h",
        "1990s": "3C64V048fGyQfCjmu9TIGA",
        "2000s": "1udqwx26htiKljZx4HwVxs",
        "2010s": "5XALIurWS8TuF6kk8bj438",
        "2020s": "6UeSakyzhiEt4NB3UAd6NQ"
    }

    # BUILD DATA (API CALLS)
    # 1) Build track-level DF
    all_dfs = []
    for decade, playlist_id in playlists_to_get.items():
        df_pl = build_playlist_tracks_df(spotify_token, playlist_id, decade, limit=5)
        if not df_pl.empty:
            all_dfs.append(df_pl)

    if all_dfs:
        df_all_tracks = pd.concat(all_dfs, ignore_index=True)
        print("All Tracks DF shape:", df_all_tracks.shape)
    else:
        df_all_tracks = pd.DataFrame()
        print("No track data from these playlists.")

    # 2) Build artists
    if not df_all_tracks.empty:
        df_artists = build_spotify_artists_df(spotify_token, df_all_tracks)
        print("Artists DF shape:", df_artists.shape)
    else:
        df_artists = pd.DataFrame()

    # 3) Build similar tracks
    if not df_all_tracks.empty and lastfm_api_key:
        df_similar_tracks = build_similar_tracks_df(spotify_token, lastfm_api_key, df_all_tracks)
        print("Similar Tracks DF shape:", df_similar_tracks.shape)
    else:
        df_similar_tracks = pd.DataFrame()

    # 4) Build similar artists
    if not df_artists.empty and lastfm_api_key:
        df_similar_artists = build_similar_artists_df(spotify_token, lastfm_api_key, df_artists)
        print("Similar Artists DF shape:", df_similar_artists.shape)
    else:
        df_similar_artists = pd.DataFrame()


    # DELETE TRACKS with mismatched decades
    df_clean_tracks = delete_mismatch_release_year(df_all_tracks)

    # EXPORT 4 CSVs into 'datasets/timestamp' folder
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join("./datasets", timestamp_str)
    tracks_name = "all_tracks.csv"
    export_csv_in_dir(df_clean_tracks, csv_path, tracks_name)
    export_csv_in_dir(df_artists, csv_path, "all_artists.csv")
    export_csv_in_dir(df_similar_tracks, csv_path,"similar_tracks.csv")
    export_csv_in_dir(df_similar_artists, csv_path,"similar_artists.csv")

    print("\nDone creating 4 CSVs in 'datasets/' folder.")

    # TRACK ANALYSIS
    print("\nAnalysis:")
    track_analysis(os.path.join(csv_path, tracks_name))


if __name__ == "__main__":
    main()
