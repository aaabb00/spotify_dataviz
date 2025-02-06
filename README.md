# Spotify Data Visualization

A **Dash + Plotly** application for exploring Spotify music data by **decade**, 
**genre**, and **personal top tracks**.

- **Initial Visualization**: Shows top tracks by decade (obtained from Spotify playlists).  
- **Spotify Login**: Allows a user to connect their Spotify account and view a second graph 
  of their personal top 50 tracks (from the last 6 months).  
- **Comparison**: Enables users to compare their personal listening habits (which 
  decades they favor) against general data.


## Disclaimer

This visualization is created for **educational** and **non-commercial** purposes, 
using data from the **Spotify API** and the **Last.fm API**:

- **Spotify API**: Used to retrieve track and artist data, hyperlinks, and images.  
- **Last.fm API**: Used for “similar tracks” and “artist recommendations,” due to the 
  deprecation of certain Spotify API features (see [Spotify API Changes, Nov. 2024](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api)).

**Spotify** retains all rights to the data and brand assets provided through their API.  
**Last.fm** is credited for recommendation data, per their terms of use.


This project is not endorsed by or affiliated with Spotify. All Spotify trademarks, service marks, 
and logos are the property of Spotify. Usage here is for demonstration only.
This visualization is **solely** for exploration and learning purposes.

## User Data Privacy

- **No Server‐Side Storage**: This app does not store or retain personal data 
or tokens on any server. 
- **Session Storage**: The user’s Spotify access token is kept **client‐side** in `sessionStorage`, 
  and cleared upon logout or when the session ends.
- **Use of Tokens**:
  - **User Token**: Only used to retrieve the user’s own top tracks. 
    This token has limited scope (`user-top-read`) and is never stored server-side.
  - **App Token (Developer Credentials)**: Used for additional track/artist details 
    (original release year, artist genres, similar tracks and artists) which do not require 
    personal user data. This limits the user’s token use to only the necessary.


## Project Structure

    spotify_dataviz/
        ├── data/                  
        │   ├── analysis/              # Track analysis for general data (checking decade mismatch)
        │   ├── utils/                 # Functions calling Spotify & Last.fm and dataframe transformations
        │   ├── datasets/              # Exported CSV files
        │   └── main_general_data.py   # General decades data (tracks, artists, and similar tracks and artists) 
        ├── plotly_dash_app/
        │   ├── assets/                # CSS file
        │   ├── callbacks/             # Dash callbacks (overall and user graphs share the scatterplot template)
        │   ├── layout/
        │   │   ├── overall/           # Main dashboard layout divided into componentes
        │   │   └── details/           # Modal (pop-up) layout for track details divided into components
        │   ├── app.py                 # Main script to run Dash APP
        │   └── config.py              # Constants (Spotify logos URLs)
        ├── LICENSE.txt                # MIT License
        ├── requirements.txt
        └── README.md


## Install requirements

`pip install -r requirements.txt`


## Run Dash App

The App runs by default on: http://127.0.0.1:8888/

`python -m plotly_dash_app.app`


## Visualization interactions

* Filter for the maximum number of tracks per decade (slider)
* Filter for genres (linked scatterplot)
* Toggle song names on/off
* Search by song or artist name
* Filter for decades (linked scatterplot)


## General Data Extraction

The general data is obtained from the first 40 tracks from each playlist. For each
song searches the earliest album (to avoid showing a remastered song release) and
get a more accurate original decade for the track.

* **Playlists**: The general dataset is built from the first 40 tracks of each playlist.
* **Earliest Album**: For each song, the script searches for the earliest album release
(to avoid skewing decade data with remasters).
* **20 Valid Tracks**: Only the first 20 tracks whose original album date matches the
expected decade are kept.

Playlists used to get popular tracks by decade:

- **1960s:** '1960s Hits Classic' by Filtr Sweden (Spotify id: 4ZuX2YvKAlym0a8VozqV1U)

- **1970s:** '70s HITS | TOP 100 SONGS' by Filtr US (Spotify id: KmBulox9POMt9hOt3VV1x)

- **1980s:** '80s Hits Best of the 80s' by Crystal Music (Spotify id: 70N5mgNl3QBQB09zXoa72h)

- **1990s:** '90s HITS | TOP 100 SONGS' by Filtr US (Spotify id: 3C64V048fGyQfCjmu9TIGA)

- **2000s:** '2000s Throwbacks (Top 100 Hits)' by Unplugged (Spotify id: 1udqwx26htiKljZx4HwVxs)

- **2010s:** 'Top Hits of the 2010s' by Ryan Milowicki (Spotify id: 5XALIurWS8TuF6kk8bj438)

- **2020s:** 'Billboard Hot 100' by Billboard (Spotify id: 6UeSakyzhiEt4NB3UAd6NQ)

(See `main_general_data.py` for the script that pulls this data)

Spotify logo sources: https://newsroom.spotify.com/media-kit/logo-and-brand-assets/

## Notes

Last.fm API calls take some time, so the user graph might not immediately display
similar tracks and artists, when a track is selected.

## License

This project uses the MIT LICENSE. (See `LICENSE.txt`)
