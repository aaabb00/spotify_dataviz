# plotly_dash_app/callbacks/templates/details/parts/artists_layout.py

from dash import html

def get_artists_layout(df_artists):
    if df_artists.shape[0] == 0:
        return html.Div(html.H5("No artists were found for this song."))

    artists_div = artists_template(df_artists)

    layout = html.Div([
        html.H3("Artists:", style={"color": "#E9C46A"}),
        artists_div
    ], style={"margin-top": "1em"})

    return layout

def artists_template(df_artists, is_similar_art=False):
    text_tag = html.H5 if is_similar_art else html.H3
    image_size = "60em" if is_similar_art else "100em"
    text_color = "#D6CFB4" if is_similar_art else "#F8F4E1"
    layout = html.Div([
        *[html.Div([
            html.A(
                href=artist["artist_spotify_url"],
                target="_blank",
                children=html.Div([
                    html.Img(src=artist["artist_image_url"], width=image_size, height=image_size,
                             style={"border-radius": "50%"}),
                    text_tag(
                        artist["artist_name"],
                        style={
                            "padding-left": "0.5em"
                        }
                    )
                ], style={
                    "display": "flex",
                    "flex-direction": "row",
                    "align-items": "center"
                }),
                style={
                    "text-decoration": "none",
                    "color": text_color,
                    "padding-left": "1em"
                }
            )
        ]) for i, (_, artist) in enumerate(df_artists.iterrows())]
    ], style={"padding": "0em"})
    return layout