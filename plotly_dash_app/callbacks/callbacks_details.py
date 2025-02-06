# plotly_dash_app/callbacks/callbacks_details.py

from dash.dependencies import Input, Output, State
from plotly_dash_app.layout.details.details_template import show_track_detail


def register_callbacks_details(app, df_tracks, df_artists, df_similar_tracks, df_similar_artists):
    # GENERAL GRAPH -> SHOW TRACK DETAIL DATA
    @app.callback(
        Output("general-detail-modal", "is_open"),
        Output("general-detail-body", "children"),
        Output("scatterplot-general", "clickData"),
        Input("scatterplot-general", "clickData"),
        State("general-detail-modal", "is_open"),
        prevent_initial_call=True
    )
    def show_general_graph_details(click_data, is_open):

        return show_track_detail(click_data, is_open, df_tracks, df_artists, df_similar_tracks, df_similar_artists)


