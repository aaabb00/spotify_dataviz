import os
import requests
from dotenv import load_dotenv
from base64 import b64encode

def get_spotify_api_data():
    """
    Returns Spotify client_id, client_secret, redirect_uri from an .env file.
    """

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    if client_id and client_secret and redirect_uri:
        print("Spotify credentials loaded correctly.")
        return client_id, client_secret, redirect_uri
    else:
        missing_vars = []
        for var, var_name in zip(
            [client_id, client_secret, redirect_uri],
            ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI"]
        ):
            if var is None:
                missing_vars.append(var_name)
        print("Missing env variables:", ", ".join(missing_vars))
        return None, None, None


def get_spotify_api_token(client_id, client_secret):
    """
    Returns a Spotify Access token (client_credentials).
    """
    if not client_id or not client_secret:
        print("No valid client_id or client_secret.")
        return None

    try:
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        resp = requests.post(url, headers=headers, data=data)
        resp.raise_for_status()
        json_result = resp.json()
        return json_result["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Spotify token: {e}")
        return None
