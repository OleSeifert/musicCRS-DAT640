"""Module for parsing the user utterances."""

import datetime
import re
from typing import Tuple, Union


def extract_album_from_question(text: str) -> Union[str, None]:
    """Extracts the album name from a question.

    Is used to for the question "When was album X released?".

    Args:
        text: User utterance.

    Returns:
        Union[str, None]: Album name or None if not found.
    """
    # Regular expression pattern to match "When was album X released?"
    pattern = r"When was album (.+?) released\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the album name (X)
        album_name = match.group(1)
        return album_name

    return None


def extract_artist_from_question(text: str) -> Union[str, None]:
    """Extracts the artist name from a question.

    Is used for the question "How many albums has artist Y released?".

    Args:
        text: User utterance.

    Returns:
        Union[str, None]: Artist name or None if not found.
    """
    # Regex pattern to match "How many albums has artist Y released?"
    pattern = r"How many albums has artist (.+?) released\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the artist name (Y)
        artist_name = match.group(1)
        return artist_name

    return None


def extract_song_from_question_for_album(text: str) -> Union[str, None]:
    """Extracts the song name from a question.

    It is used for the question "Which album features song X?".

    Args:
        text: User utterance.

    Returns:
        Union[str, None]: Song name or None if not found.
    """
    # Regular expression pattern to match "Which album features song X?"
    pattern = r"Which album features song (.+?)\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the song name (X)
        song_name = match.group(1)
        return song_name

    return None


def helper_parse_release_date(date_str: str) -> Tuple[str, str]:
    """Parses the release date.

    Date is stored as a string in the database. This function should be used to
    extract the month and year from the date string.

    Args:
        date: Release date.

    Returns:
        Tuple[str, str]: Month and year of the release date.
    """
    date_format = "%Y-%m-%d %H:%M:%S %Z"

    # Parse the date
    date_obj = datetime.datetime.strptime(date_str, date_format)

    return date_obj.strftime("%B"), date_obj.year
