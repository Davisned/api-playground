from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, root_validator


class SpotifyUser(BaseModel):
    display_name: str

class SpotifyArtist(BaseModel):
    id: str
    name: str

class SpotifyAlbum(BaseModel):
    album_type: Literal["album", "single", "compilation"]
    artists: List[SpotifyArtist]
    available_markets: List[str]
    id: str
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int

class SpotifyTrack(BaseModel):
    album: SpotifyAlbum
    release_date: Optional[str]
    release_date_precision: Optional[str]
    artists: List[SpotifyArtist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    episode: Optional[bool]
    explicit: bool
    external_ids: Dict[str, str]
    id: str
    is_local: bool
    name: str
    popularity: int
    track: Optional[bool]
    track_number: int
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int

    @root_validator(allow_reuse=True)
    def _set_release_dates(cls, values):
        if 'album' in values:
            values['release_date'] = values['album'].release_date
            values['release_date_precision'] = values['album'].release_date_precision

        return values

class SpotifyPlaylist(BaseModel):
    tracks: List[SpotifyTrack]
    collaborative: bool
    description: Optional[str]
    followers: dict
    id: str
    name: str
    owner: SpotifyUser
    public: bool
