# plotly_dash_app/layouts/utils/modal_layout.py

from dash import html
import dash_bootstrap_components as dbc
from plotly_dash_app.config import SpotifyLogo

def modal_layout(modal_id, modal_body_id):
    spotify_home_url = "https://open.spotify.com"
    layout = dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle(
                html.Div([
                    html.H5("Song Details"),
                   html.Div([
                       html.H6("All links redirect in a new tab to "),
                       html.A(
                           href=spotify_home_url,
                           target="_blank",
                           children=[html.Img(src=SpotifyLogo.GREEN_URL, width="30em", style={"margin": "0.3em"}),
                                     html.H6(" Spotify")],
                           style={"color": "#D8D2C2",
                                  "display": "flex",
                                  "align-items": "center",
                                  "text-decoration": "none"})
                   ], style={"display": "flex",
                             "align-items": "center"})
                   ], style={"color": "#D8D2C2"})
            ),
            className="my-modal-header",
            style={"backgroundColor": "#1B1B1B", "color": "white"},
            close_button=True),
        dbc.ModalBody(id=modal_body_id,
                      style={"background-color": "#2C2C2C", "color": "white"})
    ],
        id=modal_id,
        is_open=False,
        centered=True,
        size="xl",
        style={
            "max-width": "none",
            "color": "black"
        }
    )
    return layout