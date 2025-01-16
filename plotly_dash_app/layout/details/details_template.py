import dash
from dash import html
from .parts.track_layout import get_track_layout
from .parts.artists_layout import get_artists_layout
from .parts.similar_tracks_layout import get_similar_tracks_layout
from .parts.similar_artists_layout import get_similar_artists_layout

def show_track_detail(click_data, is_open, df_tracks, df_artists, df_similar_tracks, df_similar_artists,
                      has_playlist_name=True):

    if click_data and "points" in click_data:
        # Get track id from click to filter rest of dataframes
        selected_track = click_data["points"][0]
        selected_track_id = selected_track["customdata"][3]
        track = df_tracks[df_tracks["track_id"] == selected_track_id].head(1).copy()
        if track.empty:
            print("Track not found")
            return True, html.Div("Details of the selected song were not found.")
        # Get track layout
        track_layout = get_track_layout(track, has_playlist_name)
        # ARTISTS: data + layout
        artist_id = track.iloc[0]["artist_id"]
        feat_artists = track.iloc[0]["feat_artists"]
        all_artist_ids = [artist_id] + [f["id"] for f in feat_artists]

        artists = df_artists[df_artists["artist_id"].isin(all_artist_ids)].copy()
        # Sort: 1) Main artist -> 2) Feat artists
        artists["sort_index"] = artists["artist_id"].apply(all_artist_ids.index)
        artists = artists.sort_values("sort_index")
        artists.drop(columns="sort_index", inplace=True)
        # Get artist layout
        artists_layout = get_artists_layout(artists)
        # SIMILAR TRACKS: data + layout
        similar_tracks = df_similar_tracks[df_similar_tracks["original_track_id"] == selected_track_id].copy()
        similar_tracks_layout = get_similar_tracks_layout(similar_tracks)
        # SIMILAR ARTISTS: data + layout
        similar_artists = df_similar_artists[df_similar_artists["original_artist_id"] == artist_id].copy()
        similar_artists_layout = get_similar_artists_layout(similar_artists)

        # BODY DETAILS
        body_details = html.Div([
            # LEFT SIDE -> TRACK + ALBUM + SIMILAR TRACKS + PLAYLIST
            html.Div([
                # TRACK DATA
                track_layout,
                # SIMILAR TRACKS
                similar_tracks_layout
            ], style={"width": "60%"}
            ),
            # RIGHT SIDE
            html.Div([
                # ARTISTS
                artists_layout,
                # SIMILAR ARTISTS
                similar_artists_layout
            ], style={"width": "40%"}
            )
        ], style={"display": "flex"})
        return True, body_details, None

    return is_open, dash.no_update, dash.no_update









