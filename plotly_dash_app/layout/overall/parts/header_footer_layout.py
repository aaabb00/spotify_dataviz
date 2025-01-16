# plotly_dash_app/layouts/utils/header_footer.py

from dash import html


def header_layout():
    """Title and subtitle definition"""
    layout = html.Div([
            # Title
            html.Div([
                html.H1("What’s your musical decade? Discover your favorite era of hits"),
            ], style={"padding-top": "1em",
                      "color": "#E7D283"}),
            # Subtitle
            html.Div([
                html.H5("Explore iconic songs across decades and uncover when your favorite tunes were at their peak.",
                        style={"color": "#F5E7B2"}),
                html.H6("Bubble sizes reflect current Spotify popularity.",
                        style={"color": "#FFEFB8"})
            ])
        ], style={"text-align": "center"})
    return layout

def footer_layout():
    """Data source information"""
    layout = html.Div([
        # USER DATA PROTECTION
        html.Div([
            html.H6("User Data Protection",
                    className="footer-title",
                    style={
                        "padding": "8em 0em 1em 0em"
                    }),
            html.P("The App does not store or retain personal data or tokens beyond the "
                   "session needed for demonstration. "),
            html.P(" - No Server‐Side Storage: This App does not store or retain personal data "
                   "or tokens on any server."),
            html.P("- Session Storage: The user’s Spotify access token is kept **client‐side** in `sessionStorage`, "
                   "and cleared upon logout or when the session ends."),
            html.P("- Use of Tokens:"),
            html.Div([
                html.P("- User Token**: Only used to retrieve the user’s own top tracks. "
                       "This token has limited scope (`user-top-read`) and is never stored server-side."),
                html.P("- App Token (Developer Credentials): Used for additional track/artist details "
                       "(original release year, artist genres, similar tracks and artists) which do not require "
                       "personal user data. This limits the user’s token use to only the necessary.")
            ], style={"padding-left": "2em"})

        ], style={"padding-top": "8em"}),
        # DATA SOURCE
        html.Div([
            html.H6("Data Source: Spotify API (December 2024)",
                    className="footer-title"),
        ], style={"padding": "1em 0em"}),
        html.Div([
            html.P("Songs are the first 30 tracks from the following playlists in Spotify:"),
            html.P(" - 1960s: '1960s Hits Classic' by Filtr Sweden (Spotify id: 4ZuX2YvKAlym0a8VozqV1U)"),
            html.P(" - 1970s: '70s HITS | TOP 100 SONGS' by Filtr US (Spotify id: KmBulox9POMt9hOt3VV1x)"),
            html.P(" - 1980s: '80s Hits Best of the 80s' by Crystal Music (Spotify id: 70N5mgNl3QBQB09zXoa72h)"),
            html.P(" - 1990s: '90s HITS | TOP 100 SONGS' by Filtr US (Spotify id: 3C64V048fGyQfCjmu9TIGA)"),
            html.P(" - 2000s: '2000s Throwbacks (Top 100 Hits)' by Unplugged (Spotify id: 1udqwx26htiKljZx4HwVxs)"),
            html.P(" - 2010s: 'Top Hits of the 2010s' by Ryan Milowicki (Spotify id: 5XALIurWS8TuF6kk8bj438)"),
            html.P(" - 2020s: 'Billboard Hot 100' by Billboard (Spotify id: 6UeSakyzhiEt4NB3UAd6NQ)")
            ]
        ),
        html.P("Spotify logo source: https://newsroom.spotify.com/media-kit/logo-and-brand-assets/"),
        # DISCLAIMER
        html.Div([
            html.H6("Disclaimer",
                    className="footer-title",
                    style={"padding": "2em 0em 1em 0em"}),
            html.Div([
                html.P([
                    "This visualization is created for educational and non-commercial purposes using data "
                    "from the Spotify API and the Last.fm API."]),
                html.P([" - Spotify API was used to retrieve track data, "
                    "artist data, hyperlinks, and images. "]),
                html.P([" - Last.fm API for similar tracks and artist recommendations "
                    "due to the deprecation of certain Spotify API features ",
                    html.A(
                        "(referenced in the Spotify API Changes Announcement, November 2024).",
                        href="https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api",
                        target="_blank",
                        style={"color": "#C8C2BC"}
                    )
                ], style={"display": "inline-block"})
            ]),
            html.P(["Spotify retains all rights to the data and brand assets provided through their API. "
                    "Last.fm is credited for the recommendation data, and their respective terms of use apply."]),
            html.P(["This visualization does not redistribute raw data and is intended solely for "
                    "exploration and learning purposes."]),
            html.P(["This project is not endorsed by or affiliated with Spotify. "
                    "Usage here is for demonstration only."])
            ]),
        ], style={"text-align": "left",
                  "padding": "0.5em 5em",
                  "font-size": "13",
                  "font-weight": "200",
                  "color": "#C8C2BC"}
    )
    return layout

