# plotly_dash_app/callbacks/templates/filter_decades_template.py

from dash import html


def create_filter_decades(selected_decades, decades):
    all_decades_selected = ("All Decades" in selected_decades)
    new_options = []
    for decade in decades:
        is_selected = (decade in selected_decades)
        new_options.append({
            "label": html.Div(
                decade,
                style={
                    "backgroundColor": "#2C3639" if decade != "All Decades" else "#0B192C",
                    "opacity": 1.0 if is_selected or all_decades_selected else 0.4,
                    "padding": "0.5em 1.3em" if decade != "All Decades" else "0.5em 1em",
                    "margin": "0",
                    "borderRadius": "4px",
                    "justify-content": "space-between",
                }),
            "value": decade,
        })
    return new_options