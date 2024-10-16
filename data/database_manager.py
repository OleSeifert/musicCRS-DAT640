"""Contains the DatabaseManager class."""

import datetime
import sqlite3
from typing import Union


class DatabaseManager:
    """Database Manager."""

    def __init__(self, db_path: str) -> None:
        """Database Manager.

        This class is used to manage the database.
        It creates a connection to the database and provides
        methods to interact with it.

        Args:
            db_path: Path to the database.
        """
        self.db_path = db_path

    def find_song_by_title_and_artist(
        self, song_title: str, artist: str = None
    ) -> Union[Song, None]:
        """Finds a song in the database by title and artist.

        Artist is optional. Returns the first song found. If the song is not
        found, returns None.

        Args:
            song_title: Song title.
            artist: Artist.

        Returns:
            Union[Song, None]: Song object or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            if artist:  # Artist is provided
                cursor.execute(
                    "SELECT * FROM music WHERE track_name=? AND artists LIKE ?",
                    (song_title, f"%{artist}%"),
                )
            else:  # Artist is not provided
                cursor.execute("SELECT * FROM music WHERE track_name=?", (song_title,))

            results = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if results:
            # TODO: Initialize the song object
            return None
        else:
            return None

    def find_album_release_date(self, album_name: str) -> Union[datetime.date, None]:
        """Fetches the release date of an album.

        If the album is not found, returns None.

        Args:
            album_name: Album name.

        Returns:
            Union[datetime.date, None]: Release date of the album or None if not
              found.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT release_date FROM music_table WHERE album_name=?", (album_name,)
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:
            return datetime.datetime.strptime(result[0], "%Y-%m-%d").date()
        return None

    def number_of_albums_by_artist(self, artist_name: str) -> Union[int, None]:
        """Fetches the number of albums by an artist.

        Returns None if the artist is not found.

        Args:
            artist_name: Artist name.

        Returns:
            Union[int, None]: Number of albums by the artist or None if not
              found.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # TODO: Fix query
            # cursor.execute(
            #     "SELECT COUNT(*) FROM music_table WHERE artists LIKE ?", (f"%{artist_name}%",)
            # )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:
            return result
        return None

    def album_for_song(self, song_title: str) -> Union[str, None]:
        """Fetches the album, which contains a song.

        Returns None if the song is not found.

        Args:
            song_title: Song title.

        Returns:
            Union[str, None]: Album for the song or None if not found.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # TODO: Fix query later
            # cursor.execute(
            #     "SELECT album_name FROM music_table WHERE track_name=?", (song_title,)
            # )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:
            return result[0]
        return None
