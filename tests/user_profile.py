"""This module contains the UserProfile class for the tests of the
playlist_agent.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserProfile:
    """Represents a user profile.

    Attributes:
        id: User ID.
        preferences: List of user preferences.
        liked_artists: List of liked artists. Defaults to None.
        disliked_arists: List of disliked artists. Defaults to None.
        goal: User goal. Defaults to "Create a playlist".
    """

    id: str
    preferences: List[str]
    liked_artists: Optional[List[str]] = None
    disliked_arists: Optional[List[str]] = None
    goal: str = "Create a playlist"  # TODO: Update goal
