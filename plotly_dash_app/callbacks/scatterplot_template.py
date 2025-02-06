# plotly_dash_app/callbacks/templates/scatterplot_template.py

import textwrap
import re
import unicodedata
import plotly.express as px


def create_scatterplot(df_tracks, genre_color_map, selected_genres=None, selected_decades=None,
    n_top=20, show_track_names=False, search_text=""):
    """
    Creates a Scatter plot (x="album_year", y="artists_followers", size="track_popularity", color="genre")
    1) Filter by decade
    2) Filter by genre
    3) Filter by n_top
    4) Filter by search_text
    5) Create graph
    """
    dff = df_tracks.copy(deep=True)
    # ----------------------------------------
    # 1) User DECADES filtering
    # ----------------------------------------

    if "All Decades" in selected_decades:
        # If user selected 'All Decades' -> don't filter
        pass
    else:
        dff = dff[dff["real_decade"].isin(selected_decades)]

    # ----------------------------------------
    # 2) User GENRES filtering
    # ----------------------------------------
    if "All Genres" in selected_genres:
        # If user selected 'All Genres' -> don't filter
        pass
    else:
        dff = dff[dff["main_genre"].isin(selected_genres)]

    # ----------------------------------------
    # 3) User TOP N TRACKS filtering
    # ----------------------------------------
    dff = dff.groupby("real_decade").head(n_top)

    # ----------------------------------------
    # 4) User SEARCH BAR text
    # ----------------------------------------
    search_text = (search_text or "").strip()
    if search_text:
        norm_search_text = normalize_text(search_text)
        dff = dff[
            dff["track_name"].apply(normalize_text).str.contains(norm_search_text, na=False) |
            dff["artist_name"].apply(normalize_text).str.contains(norm_search_text, na=False)
            ]

    # Filtered data EMPTY -> empty graph
    if len(selected_decades) == 0:
        if len(selected_genres) > 0:
            warning = "Please select a decade."
        else:
            warning = "Please select a decade and a genre."
    elif len(selected_genres) == 0:
        warning = "Please select a genre."
    else:
        warning = "There are no songs for the filters applied.<br>"\
                  "Try adding more decades or genres<br>or removing the search filter."
    if dff.empty:
        # RETURN AN EMPTY GRAPH WITH WARNING
        fig = px.scatter()
        fig.update_layout(
            plot_bgcolor="black",
            paper_bgcolor="black",
            font_color="white",
            title=dict(text=warning,
                       font=dict(size=40), x=0.6, y=0.7)
        )
        fig.update_yaxes(
            showgrid=False
        )
        fig.update_xaxes(
            showgrid=False
        )
        return fig


    # WRAP TRACK NAMES
    dff["wrapped_track_name"] = dff["track_name"].apply(lambda t: "<br>".join(textwrap.wrap(t, width=15)))

    # Verify types
    dff["album_year"] =dff["album_year"].astype(int)
    dff["artist_followers"] =dff["artist_followers"].astype(int)

    # SHOW TEXT LABEL POINT if rows < 10
    n_rows = dff.shape[0]
    show_text = n_rows < 10 or show_track_names
    if show_text:
        text_col = "wrapped_track_name" if n_rows < 10 else "track_name"
    else:
        text_col = None

    # SCALE TRACK POPULARITY FOR POINT SIZE
    dff, zoom_factor = normalize_pop_size(dff, selected_decades, n_top)
    # ----------------------------------------
    # 5) Create GRAPH with filtered data
    # ----------------------------------------
    fig = px.scatter(
        dff,
        x="album_year",
        y="artist_followers",
        size="pop_size",
        size_max=12 * zoom_factor,
        color="main_genre",
        custom_data=["track_name", "artist_name", "track_popularity", "track_id"],
        color_discrete_map=genre_color_map,
        text=text_col,
        opacity=0.8,
        height=500
    )

    # Point text formatting
    if n_rows < 1:
        fig.update_traces(marker=dict(sizemode='area'),
                          textposition='middle center')

    # Hovering text formatting
    fig.update_traces(
        hovertemplate="<br>   ".join([
            "<br> <br>",
            "<span style='color: white; font-size: 20;'><b>%{customdata[0]}  </b></span>",
            "<span style='color: white; font-size: 18;'><i>  by %{customdata[1]}</i>  <br></span>",
            "<span style='color: white; font-size: 16;'>Spotify Song Popularity %{customdata[2]}   <br> </span>"
        ]),
        marker_line_width=0
    )

    # Plot formatting
    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        showlegend=False,
        hoverlabel=dict(
            font_size=16,
            font_family="Arial"
        ),
        title=dict(text="Artist's Followers <br>in Spotify", font=dict(size=12), x=0)
    )

    fig.update_xaxes(
        title=None,
        showgrid=False,
        tickformat="d"
    )
    fig.update_yaxes(
        title=None,
        showgrid=False
    )

    # If all decades -> remove x ticks
    if ("All Decades" in selected_decades or len(selected_decades) > 6) and search_text == "":
        fig.update_xaxes(
            showticklabels=False
        )


    return fig


def normalize_pop_size(dff, selected_decades, n_top):

    max_songs_decade = dff.groupby("real_decade")["track_id"].count().max()
    n_rows = dff.shape[0]
    # Normalize (MinMax -> [0, 1])
    pop_min = dff["track_popularity"].min()
    pop_max = dff["track_popularity"].max()
    pop_range = max((pop_max - pop_min), 1)
    dff["pop_scaled"] = (dff["track_popularity"] - pop_min) / pop_range

    n_sel_decs = 0 if "All Decades" in selected_decades else len(selected_decades)
    n_sel_decs = max(n_sel_decs, 1)
    # Base factor: number of decades selected and max songs per decade
    base_factor = 5.0 / (max_songs_decade * n_sel_decs)
    # Top factor: n_top selection
    min_rows = 5
    max_rows = 20 * 7
    max_zoom = 3.0
    min_zoom = 1.5

    n_clamped = max(min_rows, min(n_rows, max_rows))

    zoom_factor = max_zoom - (n_clamped - min_rows) * (max_zoom - min_zoom) / (max_rows - min_rows)

    if n_rows < 15:
        zoom_factor *= 1.3
    if n_rows < 10:
        zoom_factor *= 1.6

    # Final size -> point size range
    base_px = 2
    max_px = 10
    dff["pop_size"] = (base_px + dff["pop_scaled"] * (max_px - base_px)) * zoom_factor
    return dff, zoom_factor


def normalize_text(text):
    text = (unicodedata.normalize('NFD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8'))
    text = text.strip().lower()
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    return text

