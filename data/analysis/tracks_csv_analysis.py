# tracks_csv_analysis.py

import os
import pandas as pd

def unique_genres(df):
    unique_genres = df["main_genre"].unique().tolist()
    print("Unique main genres:", unique_genres)

def count_tracks_per_decade(df):
    print("Total tracks per decade:")
    counts = df["real_decade"].value_counts(sort=False)
    print(counts)

def mismatch_release_year(df):
    mismatch_year = df.loc[(df["album_year"].astype(int) <
                            df["decade"].str[:4].astype(int) - 10) |
                           (df["album_year"].astype(int) >
                            df["decade"].str[:4].astype(int) + 15),
        ["track_name", "artist_name", "decade", "decade", "album_year"]
    ]
    print(f"Total wrong release year tracks: {mismatch_year.shape[0]}")
    if mismatch_year.shape[0] > 0:
        print(mismatch_year.head(10))

def delete_mismatch_release_year(df):
    clean_df = df.loc[(df["album_year"].astype(int) >
                       df["decade"].str[:4].astype(int) - 10) &
                       (df["album_year"].astype(int) <
                        df["decade"].str[:4].astype(int) + 15) &
                      (df["real_decade_prefix"].astype(int) >= 196)
    ]
    print(f"Deleted {df.shape[0] - clean_df.shape[0]} tracks from tracks dataframe (wrong release year).")
    return clean_df

def track_analysis(tracks_file):
    if os.path.isfile(tracks_file):
        df = pd.read_csv(tracks_file)
        print(df.head(1))
        print(df.info())
        unique_genres(df)
        count_tracks_per_decade(df)
        mismatch_release_year(df)
    else:
        raise FileNotFoundError(f"Path {tracks_file} is not a file")

if __name__ == "__main__":
    track_analysis()