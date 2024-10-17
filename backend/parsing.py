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


def extract_num_songs_on_album(text: str) -> Union[str, None]:
    """Extracts the album name from the question about the No. of songs.

    Is used for the question "How many songs does album X contain?".

    Args:
        text: User utterance.

    Returns:
        Album name or None if not found.
    """
    # Regular expression pattern to match "How many songs does album X contain?"
    pattern = r"How many songs does album (.+?) contain\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the album name (X)
        album_name = match.group(1)
        return album_name

    return None


def extract_album_name_for_duration(text: str) -> Union[str, None]:
    """Extracts the album name from the question about duration of an album.

    Is used for the question "How long is album X?".

    Args:
        text: User utterance.

    Returns:
        Album name or None if not found.
    """
    # Regular expression pattern to match "How long is album X?"
    pattern = r"How long is album (.+?)\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the album name (X)
        album_name = match.group(1)
        return album_name

    return None


def extract_artist_for_most_popular_song(text: str) -> Union[str, None]:
    """Extracts the artist name from the question about the most popular song.

    Is used for the question "What is the most popular song by artist X?".

    Args:
        text: User utterance.

    Returns:
        Artist name or None if not found.
    """
    # Regular expression pattern to match "What is the most popular song by artist X?"
    pattern = r"What is the most popular song by artist (.+?)\?"

    # Perform the regex search
    match = re.search(pattern, text)

    if match:
        # Extract the artist name (X)
        artist_name = match.group(1)
        return artist_name

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


def helper_convert_seconds_to_minutes(seconds: float) -> float:
    """Converts seconds to minutes.

    Is used for the song duration.

    Args:
        seconds: Duration in seconds.

    Returns:
        float: Duration in minutes.
    """
    # Round to the second decimal place
    return round(seconds / 60, 2)
