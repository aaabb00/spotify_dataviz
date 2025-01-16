# plotly_dash_app/callbacks/callbacks_user_graph.py

import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly_dash_app.callbacks.scatterplot_template import create_scatterplot
from plotly_dash_app.layout.overall.parts.filter_genres_template import create_filter_genres
from plotly_dash_app.layout.overall.parts.filter_decades_template import create_filter_decades
from plotly_dash_app.layout.details.details_template import show_track_detail


def register_callbacks_user_graph(app, genre_color_map):

    @app.callback(
        Output("user-graph-div", "style"),
        Input("user-tracks-store", "data")

    )
    def show_user_graph(user_tracks):
        if not user_tracks:
            # Do not show graph
            return {"display": "none"}
        else:
            return {"display": "block"}


    # Update GENRE options (color, opacity)
    @app.callback(
        Output("filter-genre-user", "options"),
        Input("filter-genre-user", "value")
    )
    def update_genre_options(selected_genres):
        return create_filter_genres(selected_genres, genre_color_map)

    # Update DECADE options (color, opacity)
    @app.callback(
        Output("filter-decade-user", "options"),
        Input("filter-decade-user", "value"),
        State("user-tracks-store", "data")
    )
    def update_decade_options(selected_decades, user_tracks):
        df_user_tracks = pd.DataFrame(user_tracks)
        decades = ["All Decades"]
        if not df_user_tracks.empty:
            decades += df_user_tracks["real_decade"].sort_values().unique().tolist()
        return create_filter_decades(selected_decades, decades)


    @app.callback(
        Output("scatterplot-user", "figure"),
        [
            Input("user-tracks-store", "data"),
            Input("filter-top-user", "value"),
            Input("filter-genre-user", "value"),
            Input("filter-decade-user", "value"),
            Input("toggle-track-name-user", "value"),
            Input("search-bar-user", "value")
        ],
        State("user-token-store", "data"),
    )
    def load_user_data(user_tracks, n_top, selected_genres, selected_decades, show_track_names, search_text,
                       token_data):
        """
        1) Retrieve the user token from session store
        2) Call get_user-tracks(token) -> a DF
        3) Build a plotly figure
        """
        fig = px.scatter()
        fig.update_layout(
            plot_bgcolor="black",
            paper_bgcolor="black",
            font_color="white",
            title=dict(text="",
                       font=dict(size=40), x=0.6, y=0.7)
        )
        fig.update_yaxes(
            showgrid=False
        )
        fig.update_xaxes(
            showgrid=False
        )
        if not token_data:
            # no token -> no data
            warning = "No user token found, please log in."
            fig.update_layout(
                title=dict(text=warning,
                           font=dict(size=40), x=0.6, y=0.7)
            )
            return fig

        token = token_data.strip('"') if token_data.startswith('"') else token_data
        print("Token OK")

        if not user_tracks:
            # No data
            warning = ("No user tracks found."
                       "<br>Please try to log out from Spotify in"
                       "<br>your browser, open this page in a tab"
                       "<br>and log in again.")
            fig.update_layout(
                title=dict(text=warning,
                           font=dict(size=40), x=0.6, y=0.7)
            )
            return fig

        df_user_tracks = pd.DataFrame(user_tracks)
        print(f"STORED USER TRACKS -> DF SHAPE: {df_user_tracks.shape}")
        fig = create_scatterplot(df_user_tracks, genre_color_map, selected_genres, selected_decades, n_top,
                                 show_track_names, search_text)

        return fig

    # USER GRAPH -> SHOW TRACK DETAIL DATA
    @app.callback(
        Output("user-detail-modal", "is_open"),
        Output("user-detail-body", "children"),
        Output("scatterplot-user", "clickData"),
        Input("scatterplot-user", "clickData"),
        State("user-detail-modal", "is_open"),
        State("user-tracks-store", "data"),
        State("user-artists-store", "data"),
        State("user-similar_tracks-store", "data"),
        State("user-similar_artists-store", "data"),
        prevent_initial_call=True
    )
    def show_user_graph_details(click_data, is_open,
                                user_tracks, user_artists, user_sim_tracks, user_sim_artists):

        df_user_tracks = pd.DataFrame(user_tracks) if user_tracks else pd.DataFrame()
        df_user_artists = pd.DataFrame(user_artists) if user_artists else pd.DataFrame()
        df_user_sim_tracks = pd.DataFrame(user_sim_tracks) if user_sim_tracks else pd.DataFrame()
        df_user_sim_artists = pd.DataFrame(user_sim_artists) if user_sim_artists else pd.DataFrame()

        print("User track detail cliked")
        return show_track_detail(click_data, is_open,
                                 df_user_tracks, df_user_artists, df_user_sim_tracks, df_user_sim_artists,
                                 has_playlist_name=False)