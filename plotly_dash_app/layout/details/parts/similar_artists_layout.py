# plotly_dash_app/callbacks/templates/details/parts/similar_artists_layout.py

from dash import html
from .artists_layout import artists_template


def get_similar_artists_layout(df_similar_artists):
    if df_similar_artists.shape[0] == 0:
        return html.Div(html.H5("No similar artists were found for the main artist of this song."))

    artists_div = artists_template(df_similar_artists, is_similar_art=True)

    layout = html.Div([
        html.H3("Similar Artists:", style={"color": "#E9C46A"}),
        artists_div
    ], style={"padding-top": "2em", "color": "#D6CFB4"})

    return layout