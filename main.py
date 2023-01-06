import pandas
import spotipy
import streamlit as st
import urllib.parse as urlparse

from spotipy.oauth2 import SpotifyClientCredentials

from spotify_dtos import SpotifyPlaylist


SPOTIPY_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SPOTIPY_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

DEFAULT_HEADERS = ["id", "name", "duration_ms", "popularity", "danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "tempo"]
ALL_HEADERS = ["album", "artists", "available_markets", "disc_number", "duration_ms", "episode", "explicit", "external_ids", "id", "is_local", "name", "popularity", "track", "track_number", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

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

@st.cache
def df_to_csv(df):
    return df.to_csv(sep='\t', index=False)

def get_spotify_id_from_url(url):
    return urlparse.urlparse(url).path.split('/')[-1].split('?')[0]

def main():
    import streamlit as st

    spotify_client = SpotifyClientWrapper(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

    playlist_url = st.text_input("Playlist URL", key="playlist_url",
        placeholder="https://open.spotify.com/playlist/438YM6ESLMwhuv40kIwa7g?si=7b96c620c0db44c5")

    if playlist_url:
        with st.spinner("Fetching playlist..."):
            if "playlist" not in st.session_state or \
                st.session_state["playlist"].id != get_spotify_id_from_url(playlist_url):
                st.session_state["playlist"] = spotify_client.playlist(playlist_url)

    if "playlist" in st.session_state and st.session_state["playlist"]:
        playlist: SpotifyPlaylist = st.session_state["playlist"]
        with st.expander(f"{playlist.name} ({len(playlist.tracks)} Tracks) - {playlist.followers['total']} Followers"):
            st.write(f"Playlist ID: {playlist.id}")
            st.write(f"Owned by: {playlist.owner.display_name}")
            st.write(f"{playlist.description}")

        options = st.multiselect(label="Select columns:",
            options=ALL_HEADERS,
            default=DEFAULT_HEADERS)
        
        data_frame_tracks = pandas.DataFrame(playlist.dict()["tracks"], columns=options)
        data_frame_tracks_csv = df_to_csv(data_frame_tracks)

        st.download_button("Download csv file for current selection",
            data=data_frame_tracks_csv,
            file_name=f"{playlist.name}.csv",
            mime="text/csv")
        st.dataframe(data_frame_tracks)

main()
