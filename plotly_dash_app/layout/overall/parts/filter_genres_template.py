# plotly_dash_app/callbacks/templates/filter_genres_template.py

from dash import html


def create_filter_genres(selected_genres, genre_color_map):
    new_options = []
    all_genres_selected = ("All Genres" in selected_genres)
    for genre, color in genre_color_map.items():
        is_selected = (genre in selected_genres)
        new_options.append({
            "label": html.Div(
                genre.title(),
                style={
                    "backgroundColor": color,
                    "opacity": 1.0 if is_selected or all_genres_selected else 0.4,
                    "padding": f"6px {6 / len(genre) * 20}px",
                    "margin": "0.5em",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                }),
            "value": genre,
        })
    return new_options