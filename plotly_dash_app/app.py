# plotly_dash_app/app.py
import os
import ast
import dash
import pandas as pd
import dash_bootstrap_components as dbc

from plotly_dash_app.layout.layout import build_layout
from plotly_dash_app.callbacks.callbacks_overall import register_callbacks_overall
from plotly_dash_app.callbacks.callbacks_details import register_callbacks_details
from plotly_dash_app.callbacks.callbacks_user_oauth import register_callbacks_user_oauth
from plotly_dash_app.callbacks.callbacks_user_graph import register_callbacks_user_graph
from data.utils.spotify_auth import get_spotify_api_data
from data.utils.lastfm_utils import get_lastfm_api_data

# LOAD DATASETS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "datasets")

df_tracks = pd.read_csv(os.path.join(csv_path, "all_tracks.csv"),
                        converters={"feat_artists": ast.literal_eval})
df_artists = pd.read_csv(os.path.join(csv_path, "all_artists.csv"))
df_similar_tracks = pd.read_csv(os.path.join(csv_path, "similar_tracks.csv"))
df_similar_artists = pd.read_csv(os.path.join(csv_path, "similar_artists.csv"))

# Get unique genres and decades for filtering
counts = df_tracks["main_genre"].value_counts()
unique_genres = counts[counts > 3].index.sort_values().tolist()
print(f"Genres with more than 3 songs: {unique_genres}")
genre_color_map = {
    "All Genres": "#0B192C",
    "country": "#FFA726",
    "electronic": "#3F51B5",
    "hip-hop": "#9C27B0",
    "pop":  "#66BB6A",
    "rock": "#00A8CC",
    "soul": "#EF5350",
    "other": "#B0BEC5",
}

decades = ["All Decades"]
decades += df_tracks["decade"].sort_values().unique().tolist()
# print(decades)
# print(df_tracks.columns)
# print(df_artists.columns)
# print(df_similar_tracks.columns)
# print(df_similar_artists.columns)

# CREATE APP
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = build_layout(5, 20)
# REGISTER GENERAL CALLBACKS
register_callbacks_overall(app, df_tracks, genre_color_map, decades)
register_callbacks_details(app, df_tracks, df_artists, df_similar_tracks, df_similar_artists)

# REGISTER USER CALLBACKS
env_path = "../env"
client_id, client_secret, redirect_uri = get_spotify_api_data()
lastfm_api_key = get_lastfm_api_data()
register_callbacks_user_oauth(app, server,  client_id, client_secret, redirect_uri, lastfm_api_key)
register_callbacks_user_graph(app, genre_color_map)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))  # fallback to 8888 if no port
    app.run_server(debug=True, host="0.0.0.0", port=port)
