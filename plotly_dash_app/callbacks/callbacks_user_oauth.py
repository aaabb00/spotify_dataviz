# plotly_dash_app/callbacks/callbacks_user_oauth.py

import pandas as pd
from flask import request
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import spotipy
from spotipy import SpotifyOAuth
from data.utils.spotify_auth import get_spotify_api_token
from data.utils.dataframes_spotify import build_track_df, build_spotify_artists_df
from data.utils.dataframes_lastfm import build_similar_tracks_df, build_similar_artists_df

def register_callbacks_user_oauth(app, server, client_id, client_secret, redirect_uri, lastfm_api_key):

    @app.callback(
        Output("spotify-login-div", "style"),
        Output("spotify-load-div", "style"),
        Input("user-token-store", "data")
    )
    def update_spotify_div(token_data):
        if not token_data:
            # Show LOG IN Button
            login_style={
                "color": "#FFEFB8",
                "display": "flex",
                "justify-content": "center",
                "margin": "1em"
            }
            load_style = {"display": "none"}
        else:
            # Show LOAD DATA Button
            login_style = {"display": "none"}

            load_style={
                "color": "#FFEFB8",
                "text-align": "center",
                "margin": "1em"
                }
        return login_style, load_style

    @server.route("/callback")
    def spotify_callback():
        code = request.args.get("code")
        if not code:
            return "No code from Spotify"
        sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope="user-top-read")

        token_info = sp_oauth.get_access_token(code)
        access_token = token_info["access_token"]
        if not access_token:
            return "No access_token in response"

        # Save token as sessionStorage and redirect user back to app
        script = f"""
                <script>
                sessionStorage.setItem("user-token-store", JSON.stringify("{access_token}"));
                window.location = "/";
                </script>
                """
        return script

    @app.callback(
        Output("spotify-url-redirect", "href"),
        Input("btn-spotify-login", "n_clicks"),
        State("user-token-store", "data"),
        prevent_initial_call=True
    )
    def spotify_login(n_clicks, token_data):
        if token_data:
            # Already have a token
            return PreventUpdate

        # Else -> get the login URL
        sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope="user-top-read")
        authorize_url = sp_oauth.get_authorize_url()
        return authorize_url


    @app.callback(
        Output("user-tracks-store", "data"),
        Input("btn-spotify-load", "n_clicks"),
        State("user-token-store", "data"),
        prevent_initial_call=True
    )
    def fetch_user_tracks(n_clicks, token_data):
        """
        1) If user has no token -> redirect to Spotify.
        2) If user has token -> call get_user_tracks(...)
           -  store the tracks in user-tracks-store (dcc.Store)
           -  if empty -> None
        """
        if not token_data:
            # Token expired -> Do not update
            raise PreventUpdate
        else:
            # USER TOKEN -> TOP TRACKS
            user_token = token_data.strip('"')
            sp = spotipy.Spotify(auth=user_token)
            user_results = sp.current_user_top_tracks(limit=20)
            items = user_results.get("items", [])

            # APP TOKEN to get info about tracks
            s_token = get_spotify_api_token(client_id, client_secret)
            items_id = [t.get("id", "") for t in items]
            df_user_tracks = build_track_df(s_token, items, items_id)
            if not df_user_tracks.empty:
                print("User Tracks DF shape:", df_user_tracks.shape)
            else:
                print("No track data from user tracks.")
                return None

            # Store user tracks in JSON (dcc.Store)
            return df_user_tracks.to_dict("records")

    @app.callback(
        Output("user-artists-store", "data"),
        Output("user-similar_tracks-store", "data"),
        Output("user-similar_artists-store", "data"),
        Input("user-tracks-store", "data"),
        State("user-token-store", "data"),
        prevent_initial_call=True
    )
    def fetch_user_related_data(user_tracks_data, token_data):
        """
        1) When user-tracks-store is updated,
           fetches user artists, similar tracks, similar artists
           and stores them in their dcc.Stores.
        2) If user_tracks_data is None.
        """

        if not token_data or not user_tracks_data:
            # no token -> can't fetch
            return None, None, None

        token_str = token_data.strip('"')
        df_user_tracks = pd.DataFrame(user_tracks_data)
        if df_user_tracks.empty:
            return None, None, None

        # App token to get info about items
        s_token = get_spotify_api_token(client_id, client_secret)
        df_user_artists = build_spotify_artists_df(s_token, df_user_tracks)
        if not df_user_artists.empty:
            print("User Artists DF shape:", df_user_artists.shape)
        else:
            return None, None, None

        # Use App token to get info about tracks
        spotify_token = get_spotify_api_token(client_id, client_secret)

        if not df_user_tracks.empty and lastfm_api_key:
            df_user_sim_tracks = build_similar_tracks_df(spotify_token, lastfm_api_key, df_user_tracks)
            print("Similar Tracks DF shape:", df_user_sim_tracks.shape)
        else:
            df_user_sim_tracks = pd.DataFrame()

        # Build similar artists
        if not df_user_artists.empty and lastfm_api_key:
            df_user_sim_artists = build_similar_artists_df(spotify_token, lastfm_api_key, df_user_artists)
            print("Similar Artists DF shape:", df_user_sim_artists.shape)
        else:
            df_user_sim_artists = pd.DataFrame()

        return (df_user_artists.to_dict("records"),
                df_user_sim_tracks.to_dict("records"),
                df_user_sim_artists.to_dict("records"))
