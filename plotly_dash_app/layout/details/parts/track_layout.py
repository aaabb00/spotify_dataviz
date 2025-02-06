# plotly_dash_app/callbacks/templates/details/parts/track_layout.py

from dash import html

def get_track_layout(track, has_playlist_name=True):
    # DATA
    track_name = track.iloc[0]["track_name"]
    track_spotify_url = track.iloc[0]["track_spotify_url"]

    album_name = track.iloc[0]["album_name"]
    album_year = track.iloc[0]["album_year"]
    album_image_url = track.iloc[0]["album_image_url"]
    album_spotify_url = track.iloc[0]["album_spotify_url"]

    playlist_name = track.iloc[0]["playlist_name"] if has_playlist_name else None
    playlist_spotify_url = track.iloc[0]["playlist_spotify_url"] if has_playlist_name else None
    playlist_layout = get_playlist_layout(has_playlist_name, playlist_name, playlist_spotify_url)

    # LAYOUT
    layout = html.Div([
        html.Div([
            html.A(
                href=track_spotify_url,
                target="_blank",
                children=[html.H1(track_name)],
                style={"color": "#F8F4E1",
                       "text-decoration": "none"
                       }
            )
        ]),
        # ALBUM
        html.Div([
            html.A(
                href=album_spotify_url,
                target="_blank",
                children=[html.Img(src=album_image_url, width="150em")]
            ),
            html.Div([
                html.A(
                    href=album_spotify_url,
                    target="_blank",
                    children=[html.H3(album_name)],
                    style={
                        "color": "#FFF7D1",
                        "margin": "1em",
                        "text-decoration": "none"
                    }
                ),
                html.H5(f"({album_year})", style={"color": "#FFF7D1"})
            ], style={"display": "block",
                      "margin-left": "1em"})
        ], style={
            "display": "flex",
            "align-items": "center"
        }),
        # PLAYLIST
        playlist_layout
    ])

    return layout

def get_playlist_layout(has_playlist_name, playlist_name=None, playlist_url=None):
    if has_playlist_name and playlist_name and playlist_url:
        layout = html.Div([
            html.H5("From Spotify playlist:"),
            html.A(
                href=playlist_url,
                target="_blank",
                children=[html.H5(playlist_name)],
                style={"margin": "1em",
                       "color": "#D0DDD0",
                       "text-decoration": "none"
                       }
            )
        ], style={
            "display": "flex",
            "align-items": "center",
            "color": "#D0DDD0",
            "padding": "0.5em"
        })
    else:
        layout = html.Div()
    return layout
