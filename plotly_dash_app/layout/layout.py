from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from plotly_dash_app.layout.overall.parts.header_footer_layout import  header_layout, footer_layout
from plotly_dash_app.layout.overall.parts.graph_layout import graph_layout
from plotly_dash_app.layout.overall.parts.modal_layout import modal_layout
from plotly_dash_app.config import SpotifyLogo


def build_layout(min_top, max_top):

    layout = html.Div([
        header_layout(),
        modal_layout("general-detail-modal", "general-detail-body"),
        # GRAPH GENERAL
        graph_layout("scatterplot-general", "filter-top", "filter-genre",
                     "filter-decade", "toggle-track-name",
                     "search-bar", "loading-general", min_top, max_top),
        # SPOTIFY AREA
        html.Div([
            # SPOTIFY LOG IN
            html.Div([
                html.H6("Still not sure? Check your Spotify top tracks", style={"margin": "1em"}),
                dbc.Button(["Login with Spotify",
                            html.Img(src=SpotifyLogo.BLACK_URL, width="30em",
                                     style={"margin": "0.3em"})],
                           id="btn-spotify-login", n_clicks=0,
                           style={
                               "background-color": "#1DB954",
                               "color": "#FFEFB8",
                               "border-radius": "18em",
                               "border": "0px solid #1DB954"
                           }),

            ],
                id="spotify-login-div",
                style={}    # Updated with callback
            ),
            # SPOTIFY LOAD DATA
            html.Div([
                html.Div([
                    html.H3("SEE YOUR TOP 20 TRACKS IN THE LAST 6 MONTHS",
                            style={"margin": "1em"}),
                    dbc.Button(["LOAD MY DATA"],
                               id="btn-spotify-load", n_clicks=0,
                               style={
                                   "background-color": "#57A6A1",
                                   "color": "#FFEFB8",
                                   "border-radius": "18em",
                                   "border": "0px solid #1DB954",
                                   "padding": "1em 2em",
                                   "height": "150%"
                               }),
                ], style={
                "color": "#FFEFB8",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "margin": "1em"
            }),
                html.P("Last.fm API calls take a while, so it may not immediately show "
                       "similar tracks and artists data. Wait a few minutes before selecting a song."
                       "or uploading data.",
                        style={"margin": "1em",
                               "font-size": "14"}),
            ],
                id="spotify-load-div",
                style={} # Updated with callback
            ),

            dcc.Location(id="spotify-url-redirect", refresh=True),
            dcc.Store(id="user-token-store", storage_type="session"),
            dcc.Store(id="user-tracks-store", storage_type="session"),
            dcc.Store(id="user-artists-store", storage_type="session"),
            dcc.Store(id="user-similar_tracks-store", storage_type="session"),
            dcc.Store(id="user-similar_artists-store", storage_type="session")
        ]),
        modal_layout("user-detail-modal", "user-detail-body"),

        html.Div(
            [graph_layout("scatterplot-user", "filter-top-user", "filter-genre-user",
                     "filter-decade-user", "toggle-track-name-user",
                     "search-bar-user", "loading-user", min_top, max_top)],
            id="user-graph-div",
            style={"display": "none"}    # hidden by default -> updated callback (if token -> show)
        ),
        # FOOTER: DATA SOURCE
        footer_layout()
    ], style={
        "background-color": "black",
        "color": "white",
        "font-family": "Arial, sans-serif"
    })
    return layout



