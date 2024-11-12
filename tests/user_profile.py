"""This module contains the UserProfile class for the tests of the
playlist_agent.
"""

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
        goal: User goal. Defaults to "Create a playlist".
    """

    id: str
    preferences: List[str]
    prefered_artists: List[str]
    prefered_songs: List[str]
    goal: str = "Create a playlist"
