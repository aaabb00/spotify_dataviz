# plotly_dash_app/callbacks/templates/details/parts/similar_tracks_layout.py

from dash import html


def get_similar_tracks_layout(df_similar_tracks):
    if df_similar_tracks.shape[0] == 0:
        return html.Div(html.H5("No similar songs were found for this song."))

    layout = html.Div([
        html.H3("Similar Tracks:",
                style={
                    "padding": "1em 0em 0.5em 0em",
                    "color": "#E9C46A"}),
        *[html.Div([
            html.H5(i + 1, style={
                "width": "2em",
                "height": "2em",
                "border-radius": "50%",
                "background-color": "#66490D",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center"

            }),
            html.A(
                href=track["track_spotify_url"],
                target="_blank",
                children=[html.H4(track["track_name"])],
                style={
                    "color": "#D6CFB4",
                    "margin-left": "1em",
                    "text-decoration": "none"
                }),
            html.H4(["by", html.I(track["artist_name"], style={"margin-left": "0.4em"})],
                    style={"margin-left": "0.4em", "font-weight": "200"})
        ], style={"display": "flex",
                  "align-items": "center",
                  "margin": "1em"})
            for i, (_, track) in enumerate(df_similar_tracks.iterrows())]
    ], style={"margin-top": "1em",
              "color": "#D6CFB4"})

    return layout