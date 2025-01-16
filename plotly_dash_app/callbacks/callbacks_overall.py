# plotly_dash_app/callbacks/callbacks_overall.py

from dash.dependencies import Input, Output
from plotly_dash_app.callbacks.scatterplot_template import  create_scatterplot
from plotly_dash_app.layout.overall.parts.filter_genres_template import create_filter_genres
from plotly_dash_app.layout.overall.parts.filter_decades_template import create_filter_decades

def register_callbacks_overall(app, df_tracks, genre_color_map, decades):

    # Update GENRE options (color, opacity)
    @app.callback(
        Output("filter-genre", "options"),
        Input("filter-genre", "value")
    )
    def update_genre_options(selected_genres):
        return create_filter_genres(selected_genres, genre_color_map)


    # Update DECADE options (color, opacity)
    @app.callback(
        Output("filter-decade", "options"),
        Input("filter-decade", "value")
    )
    def update_decade_options(selected_decades):
        return create_filter_decades(selected_decades, decades)

    @app.callback(
        Output("scatterplot-general", "figure"),
        [
            Input("filter-top", "value"),
            Input("filter-genre", "value"),
            Input("filter-decade", "value"),
            Input("toggle-track-name", "value"),
            Input("search-bar", "value")
        ]
    )
    # Update GRAPH
    def update_scatterplot(n_top, selected_genres, selected_decades, show_track_names, search_text):

        fig = create_scatterplot(df_tracks, genre_color_map, selected_genres, selected_decades, n_top,
                                 show_track_names, search_text)

        return fig


