# plotly_dash_app/layouts/utils/graph_layout.py


from dash import dcc
from dash import html
import dash_daq as daq


def graph_layout(graph_id, filter_top_id, filter_genre_id, filter_decade_id,
                 toggle_id, search_bar_id, loading_id, min_top=1, max_top=20):
    layout = html.Div([
        # Graph TOP FILTERING
        html.Div([
            # TOP TRACK FILTER
            html.Div([
                html.Label("Top tracks per decade"),
                dcc.Slider(
                    id=filter_top_id,
                    min=min_top,
                    max=max_top,
                    step=5,
                    value=max_top,
                    marks={i: {'label': str(i), 'style': {'color': '#B9E5E8'}} for i in range(min_top, max_top + 1, 5)}
                )
            ], style={
                "padding-bottom": "1em",
                "padding-left": "9em",
                "width": "30%",
                "color": "#B9E5E8"
            }),
            # GENRES FILTER
            html.Div([
                dcc.Checklist(
                    id=filter_genre_id,
                    options=[],  # Fill with callback
                    value=["All Genres"],
                    inline=True,
                    inputStyle={"display": "none"}
                )
            ], style={
                "padding": "0 1em"
            }),
        ], style={
            "display": "flex",
            "flex-direction": "row",
            "alignItems": "center",
            "padding": "1em 2em 0em 0em"
        }),
        # SHOW TRACK NAME + SEARCH BAR
        html.Div(
            # SHOW TRACK NAME FILTER
            html.Div([
                html.Div([
                    html.P("Show track names", style={"color": "#D9DFC6"}),
                    daq.ToggleSwitch(
                        id=toggle_id,
                        value=False
                    )
                ], style={
                    "display": "flex",
                    "flex-direction": "row",
                    "margin": "1em 4em 0em 0em"
                }),
                dcc.Input(id=search_bar_id,
                          type="text",
                          placeholder="Search artist or song...",
                          className="search-input",
                          style={
                              "width": "15em",
                              "background-color": "black",
                              "color": "white",
                              "border": "0px solid gray"
                          })
            ], style={
                "display": "flex",
                "justify-content": "flex-end",
                "align-items": "center",
                "margin": "0em 2em 1em 0em",
                "width": "88%"
            })
        ),
        html.Div([
            # GRAPH
            html.Center(
                # LOADING INTERACTION
                dcc.Loading([
                    html.Div([
                        dcc.Graph(id=graph_id),
                    ], style={
                        "width": "80%",
                        "height": "100%"
                    })
                ],
                    id=loading_id,
                    type="default"
                )
            ),
            # DECADE FILTER
            html.Div([
                dcc.Checklist(
                    id=filter_decade_id,
                    options=[],  # Fill with callback
                    value=["All Decades"],
                    inline=True,
                    inputStyle={"display": "none"},
                    labelStyle={
                        "margin": "0 0.5em",
                        "padding": "0.3em",
                    },
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "width": "85%"
                    }
                )
            ], style={
                "position": "absolute",
                "top": "88%",
                "left": "2em",
                "right": "1em",
                "display": "flex",
                "justify-content": "space-between",
                "align-items": "center",
                "padding": "0 1em"
            })
        ], style={
            "position": "relative",
            "height": "140%",
            "margin": "0 auto",
            "background-color": "black"
        })
    ])
    return layout