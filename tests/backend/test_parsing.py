"""Tests for the parsing module."""

from typing import Tuple

import pytest
from backend import parsing


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("When was album Thriller released?", "Thriller"),
        (
            "When was album The Dark Side of the Moon released?",
            "The Dark Side of the Moon",
        ),
        ("When was album The Wall released?", "The Wall"),
        ("When was album 1989 released?", "1989"),
    ],
)
def test_extract_album_from_question(question: str, expected: str) -> None:
    """Tests the extraction with a bunch of valid albums."""
    album = parsing.extract_album_from_question(question)
    assert album == expected


def test_extract_album_from_question_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_album_from_question("When was album released?")
    assert album is None


def test_extract_album_from_question_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_album_from_question("How many songs has artist released?")
    assert album is None


def test_extract_album_from_question_empty() -> None:
    """Tests the extraction with an empty question."""
    album = parsing.extract_album_from_question("")
    assert album is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("How many albums has artist Michael Jackson released?", "Michael Jackson"),
        ("How many albums has artist Pink Floyd released?", "Pink Floyd"),
        ("How many albums has artist Taylor Swift released?", "Taylor Swift"),
        ("How many albums has artist Queen released?", "Queen"),
    ],
)
def test_extract_artist_from_question(text: str, expected: str) -> None:
    """Tests the extraction with a question that matches."""
    artist = parsing.extract_artist_from_question(text)
    assert artist == expected


def test_extract_artist_from_question_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    artist = parsing.extract_artist_from_question("How many albums has released?")
    assert artist is None


def test_extract_artist_from_question_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    artist = parsing.extract_artist_from_question("When was album released?")
    assert artist is None


def test_extract_artist_from_question_empty() -> None:
    """Tests the extraction with an empty question."""
    artist = parsing.extract_artist_from_question("")
    assert artist is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Which album features song Billie Jean?", "Billie Jean"),
        ("Which album features song 181?", "181"),
        ("Which album features song Blank Space?", "Blank Space"),
        ("Which album features song Bohemian Rhapsody?", "Bohemian Rhapsody"),
    ],
)
def test_song_from_question_for_album(text: str, expected: str) -> None:
    """Tests the extraction with a question that matches."""
    album = parsing.extract_song_from_question_for_album(text)
    assert album == expected


def test_song_from_question_for_album_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_song_from_question_for_album("Which album features song?")
    assert album is None


def test_song_from_question_for_album_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_song_from_question_for_album(
        "How many albums has artist released?"
    )
    assert album is None


def test_song_from_question_for_album_empty() -> None:
    """Tests the extraction with an empty question."""
    album = parsing.extract_song_from_question_for_album("")
    assert album is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("How many songs does album Thriller contain?", "Thriller"),
        (
            "How many songs does album The Dark Side of the Moon contain?",
            "The Dark Side of the Moon",
        ),
        ("How many songs does album The Wall contain?", "The Wall"),
        ("How many songs does album 1989 contain?", "1989"),
    ],
)
def test_extract_num_songs_on_album(text: str, expected: str) -> None:
    """Tests the extraction with a question that matches."""
    album = parsing.extract_num_songs_on_album(text)
    assert album == expected


def test_extract_num_songs_on_album_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_num_songs_on_album("How many songs does album contain?")
    assert album is None


def test_extract_num_songs_on_album_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_num_songs_on_album("When was album released?")
    assert album is None


def test_extract_num_songs_on_album_empty() -> None:
    """Tests the extraction with an empty question."""
    album = parsing.extract_num_songs_on_album("")
    assert album is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("How long is album Thriller?", "Thriller"),
        ("How long is album The Dark Side of the Moon?", "The Dark Side of the Moon"),
        ("How long is album The Wall?", "The Wall"),
        ("How long is album 1989?", "1989"),
    ],
)
def test_extract_album_name_for_duration(text: str, expected: str) -> None:
    """Tests the extraction with a question that matches."""
    album = parsing.extract_album_name_for_duration(text)
    assert album == expected


def test_extract_album_name_for_duration_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_album_name_for_duration("How long is album?")
    assert album is None


def test_extract_album_name_for_duration_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    album = parsing.extract_album_name_for_duration("When was album released?")
    assert album is None


def test_extract_album_name_for_duration_empty() -> None:
    """Tests the extraction with an empty question."""
    album = parsing.extract_album_name_for_duration("")
    assert album is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("What is the most popular song by artist Michael Jackson?", "Michael Jackson"),
        ("What is the most popular song by artist Pink Floyd?", "Pink Floyd"),
        ("What is the most popular song by artist Taylor Swift?", "Taylor Swift"),
        ("What is the most popular song by artist Queen?", "Queen"),
        ("What is the most popular song by artist 50 Cent?", "50 Cent"),
    ],
)
def test_extract_artist_for_most_popular_song(text: str, expected: str) -> None:
    """Tests the extraction with a question that matches."""
    artist = parsing.extract_artist_for_most_popular_song(text)
    assert artist == expected


def test_extract_artist_for_most_popular_song_no_match() -> None:
    """Tests the extraction with a question that doesn't match."""
    artist = parsing.extract_artist_for_most_popular_song(
        "What is the most popular song by artist?"
    )
    assert artist is None


def test_extract_artist_for_most_popular_song_wrong_question() -> None:
    """Tests the extraction with a question that doesn't match."""
    artist = parsing.extract_artist_for_most_popular_song("When was album released?")
    assert artist is None


def test_extract_artist_for_most_popular_song_empty() -> None:
    """Tests the extraction with an empty question."""
    artist = parsing.extract_artist_for_most_popular_song("")
    assert artist is None


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ("2023-04-15 00:00:00 UTC", ("April", 2023)),
        ("2023-01-15 00:00:00 UTC", ("January", 2023)),
        ("1998-12-15 00:00:00 UTC", ("December", 1998)),
    ],
)
def test_helper_parse_release_date(date: str, expected: Tuple[str, int]) -> None:
    """Tests the helper function for parsing valid release dates."""
    parsed_date = parsing.helper_parse_release_date(date)
    assert parsed_date == expected


def test_helper_parse_release_date_invalid() -> None:
    """Tests the helper function for parsing invalid release dates.

    The function should raise a value error.
    """
    with pytest.raises(ValueError):
        parsing.helper_parse_release_date("invalid")


@pytest.mark.parametrize(
    ("seconds", "expected_minutes"),
    [
        (60, 1),
        (120, 2),
        (180, 3),
        (240, 4),
        (178.9, 2.98),
    ],
)
def test_helper_convert_seconds_to_minutes(
    seconds: float, expected_minutes: float
) -> None:
    """Tests the helper function for converting seconds to minutes."""
    minutes = parsing.helper_convert_seconds_to_minutes(seconds)
    assert minutes == expected_minutes
