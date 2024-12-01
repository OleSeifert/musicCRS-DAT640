"""The UserProfile for the simulation of the playlist_agent."""

from dataclasses import dataclass
from typing import List


@dataclass
class UserProfile:
    """Represents a user profile.

    Attributes:
        id: User ID.
        preferences: List of user preferred Song by Artist.
        prefered_artists: List of user preferred artists.
        prefered_songs: List of user preferred songs.
        goal: User goal. In our case a number of songs to add to the playlist.
    """

    id: str
    preferences: List[str]
    prefered_artists: List[str]
    prefered_songs: List[str]
    goal: int
