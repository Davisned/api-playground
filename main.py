from typing import Optional
import pandas
import spotipy
import streamlit as st
import urllib.parse as urlparse

from spotipy.oauth2 import SpotifyClientCredentials

from spotify_dtos import SpotifyPlaylist


SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""

MAX_COLS_PER_ROW = 2
MAX_TOTAL_COLS = 6

DEFAULT_HEADERS = ["id", "name", "duration_ms", "popularity", "danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "tempo"]
ALL_HEADERS = ["album", "artists", "available_markets", "disc_number", "duration_ms", "episode", "explicit", "external_ids", "id", "is_local", "name", "popularity", "track", "track_number", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

ALL_CHART_TYPES = ["line", "area", "bar"]
DEFAULT_CHART_TYPE = "line"

class SpotifyClientWrapper():
    def __init__(self, auth_manager):
        self.spc = spotipy.Spotify(auth_manager=auth_manager)

    def playlist(self, playlist_id, fields=None, market=None, additional_types=("track",)) -> SpotifyPlaylist:
        super_playlist = self.spc.playlist(playlist_id, fields, market, additional_types)
        super_playlist["tracks"] = [self.track(tr['track']['id']) for tr in super_playlist["tracks"]["items"]]
        return SpotifyPlaylist(**super_playlist)

    def track(self, track_id, market=None):
        super_track = self.spc.track(track_id, market)
        st_with_features = {**super_track, **self.spc.audio_features([track_id])[0]}
        return st_with_features

st.set_page_config(layout="wide")
st.markdown(f"""
<style>
button[title="View fullscreen"] {{
    right: 0;
    top: -0.75rem;
}}
details[title="Click to view actions"] {{
    right: 0;
    bottom: 13.375rem;
    position: sticky;
}}
</style>""", unsafe_allow_html=True)

if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET:
    auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
else:
    auth_manager = SpotifyClientCredentials()

spotify_client = SpotifyClientWrapper(auth_manager=auth_manager)

@st.cache
def df_to_csv(df):
    return df.to_csv(sep='\t', index=False)

@st.cache
def get_playlist(url):
    return spotify_client.playlist(url)

def add_new_tab():
    if "columns" not in st.session_state:
        st.session_state["columns"] = [
            {
                "column_id": 0,
                "playlist": None
            }
        ]
    else:
        st.session_state["columns"].append({
            "column_id": len(st.session_state["columns"]),
            "playlist": None
        })

def get_chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_spotify_id_from_url(url):
    return urlparse.urlparse(url).path.split('/')[-1].split('?')[0]

def get_column_by_id(id):
    if "columns" not in st.session_state:
        return None

    for col in st.session_state["columns"]:
        if col["column_id"] == id:
            return col

    return None

def remove_column_by_id(id):
    if "columns" not in st.session_state:
        return

    for col in st.session_state["columns"]:
        if col["column_id"] == id:
            index = st.session_state["columns"].index(col)
            del st.session_state["columns"][index]

def main(column, index):
    import streamlit as st

    with column:
        playlist: Optional[SpotifyPlaylist] = get_column_by_id(index)["playlist"]
        column_id: int = get_column_by_id(index)["column_id"]

        playlist_url = st.text_input("Playlist URL", key=f"playlist_url_{column_id}",
            placeholder="https://open.spotify.com/playlist/438YM6ESLMwhuv40kIwa7g?si=7b96c620c0db44c5")

        if playlist_url and (playlist is None or playlist.id != get_spotify_id_from_url(playlist_url)):
            with st.spinner("Fetching playlist..."):
                try:
                    get_column_by_id(column_id)["playlist"] = get_playlist(playlist_url)
                    playlist = get_column_by_id(column_id)["playlist"]
                except TypeError:
                    st.write("Could not load playlist. Probably not public.")
        
        if playlist:
            with st.expander(f"{playlist.name} ({len(playlist.tracks)} Tracks) - {playlist.followers['total']} Followers"):
                st.write(f"Playlist ID: {playlist.id}")
                st.write(f"Owned by: {playlist.owner.display_name}")
                st.write(f"{playlist.description}")
            
            data_frame_tracks = pandas.DataFrame(playlist.dict()["tracks"])
            data_frame_tracks_csv = df_to_csv(data_frame_tracks)

            with st.expander(f"Table View"):
                options = st.multiselect(label="Select columns:",
                    key=f"column_select_{column_id}",
                    options=ALL_HEADERS,
                    default=DEFAULT_HEADERS)
                st.download_button("Download csv file for current selection",
                    key=f"download_bttn_{column_id}",
                    data=data_frame_tracks_csv,
                    file_name=f"{playlist.name}.csv",
                    mime="text/csv")
                st.dataframe(data_frame_tracks[options])

            with st.expander(f"Chart View"):
                with st.container():
                    chart_type = st.selectbox(label="Select chart type.",
                        key=f"chart_type_{column_id}",
                        options=ALL_CHART_TYPES,
                        index=0
                    )

                    y_axis = st.selectbox(label="Y Axis",
                        key=f"y_axis_{column_id}",
                        options=ALL_HEADERS,
                        index=ALL_HEADERS.index("popularity")
                    )
                    x_axis = st.selectbox(label="X Axis",
                        key=f"x_axis_{column_id}",
                        options=ALL_HEADERS,
                        index=ALL_HEADERS.index("name")
                    )

                    if chart_type == "line":
                        st.line_chart(data_frame_tracks, x=x_axis, y=y_axis)
                    elif chart_type == "area":
                        st.area_chart(data_frame_tracks, x=x_axis, y=y_axis)
                    else: # chart_type == "bar":
                        st.bar_chart(data_frame_tracks, x=x_axis, y=y_axis)
            

        if st.button("Close",
            disabled=(column_id == 0),
            on_click=remove_column_by_id,
            args=[column_id],
            key=f"bttn_close_{column_id}"):
            return

if "columns" not in st.session_state:
    add_new_tab()

all_columns = st.session_state["columns"]
total_cols = len(all_columns)

with st.container():
    for chunk in get_chunk(all_columns, MAX_COLS_PER_ROW):
        columns = st.columns(len(chunk))

        for pack in zip(columns, chunk):
            main(pack[0], pack[1]["column_id"])

        st.markdown("<hr/>", unsafe_allow_html=True)

with st.container():
    if st.button("New Tab \U0001f995", disabled=(total_cols>MAX_TOTAL_COLS), on_click=add_new_tab):
        # st.experimental_rerun()
        pass
