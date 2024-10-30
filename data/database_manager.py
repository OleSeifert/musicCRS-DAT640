"""Contains the DatabaseManager class."""

import os
import sqlite3
from typing import List, Tuple, Union

from models.song import Song


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
        self.db_path = os.path.abspath(db_path)

    def find_song_by_title_and_artist_both_given(
        self, song_title: str, artist: str
    ) -> Union[List[Song], None]:
        """Finds a song in the database by title and artist.

        Only gets called if both song title and artist are given.

        Args:
            song_title: Song title.
            artist: Artist name.

        Returns:
            A list of song objects if found, otherwise None.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # First try correct spelling
        try:
            cursor.execute(
                "SELECT * FROM music WHERE track_name=? AND artist_0=?",
                (song_title, artist),
            )
            # Assuming that each song by an artist is unique
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:
            if len(result) == 1:
                return [result]
            return [Song(*result)]

        # If the song is not found, try the alternative spellings
        results = self.fetch_transformed_songs_by_artist(song_title, artist)

        if results:
            if len(results) == 1:
                return [results[0]]
            return results
        return None

    def find_song_only_by_title(self, song_title: str) -> Union[List[Song], None]:
        """Finds a song in the database by title only.

        It first tries to find the song by the correct spelling. If the song is
        not found, it tries to find the song by the alternative spellings.o

        Args:
            song_title: Song title.

        Returns:
            A list of song objects if found, otherwise None.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Try correct spelling first
        try:
            cursor.execute("SELECT * FROM music WHERE track_name=?", (song_title,))
            results = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if results:
            if len(results) == 1:
                return [Song(results[0])]
            return [Song(*result) for result in results]

        # If the song is not found, try the alternative spellings
        songs = self.fetch_transformed_songs_by_title(song_title)

        if songs:
            return songs
        return None

    def find_album_release_date(self, album_name: str) -> Union[str, None]:
        """Fetches the release date of an album.

        If the album is not found, returns None.

        Args:
            album_name: Album name.

        Returns:
            Release date of the album as a string or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT release_date FROM music WHERE album_name=?", (album_name,)
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:
            print(result)
            return result[0]
        return None

    def number_of_albums_by_artist(self, artist_name: str) -> Union[int, None]:
        """Fetches the number of albums by an artist.

        Returns None if the artist is not found.

        Args:
            artist_name: Artist name.

        Returns:
            Number of albums by the artist or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT COUNT(DISTINCT album_id) FROM music WHERE artist_0=?",
                (artist_name,),
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        if result[0] > 0 and result:
            cursor.close()
            connection.close()
            return result[0]
        # Try with alternative spellings
        artist_id = self.fetch_transformed_artist_id(artist_name)

        if artist_id:  # Fetch the number of albums
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "SELECT COUNT(DISTINCT album_id) FROM music WHERE artist_id=?",
                    (artist_id,),
                )
                result = cursor.fetchone()

            except sqlite3.Error as e:
                print(f"Error: {e}")
                return None

            finally:  # Tear down
                cursor.close()
                connection.close()

            if result:
                return result[0]
            return None

        return None

    def number_of_songs_on_album(self, album_name: str) -> Union[int, None]:
        """Fetches the number of songs on an album.

        Args:
            album_name: Album name.

        Returns:
            Number of songs on the album or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT total_tracks FROM music WHERE album_name=?",
                (album_name,),
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:
            return result[0]

        return None

    def duration_of_album(self, album_name: str) -> Union[float, None]:
        """Fetches the duration of an album.

        The duration is in seconds.

        Args:
            album_name: Album name.

        Returns:
            Duration of the album or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # First get the album_id
            album_id = self.get_id_for_album(album_name)
            if album_id:
                cursor.execute(
                    "SELECT SUM(duration_sec) FROM music WHERE album_id=?",
                    (album_id,),
                )
                result = cursor.fetchone()
            else:
                return None

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:
            return result[0]

        return None

    def most_popular_song_by_artist(self, artist_name: str) -> Union[str, None]:
        """Fetches the most popular song by an artist.

        It uses the function get_artist_id to get the artist ID. The most
        popular song is fetched by the artist ID.

        Args:
            artist_name: Artist name.

        Returns:
            Most popular song by the artist or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            artist_id = self.get_id_for_artist(artist_name)

            if artist_id:
                cursor.execute(
                    "SELECT track_name FROM music WHERE artist_id=? ORDER BY track_popularity DESC",
                    (artist_id,),
                )
                result = cursor.fetchone()
            else:  # Try with alternative spelling
                artist_id = self.fetch_transformed_artist_id(artist_name)
                if artist_id:
                    cursor.execute(
                        "SELECT track_name FROM music WHERE artist_id=? ORDER BY track_popularity DESC",
                        (artist_id,),
                    )
                    result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:  # Will never not set
            return result[0]
        return None

    def get_id_for_album(self, album_name: str) -> Union[str, None]:
        """Fetches the ID for an album.

        It is used to help the duration_of_album method.

        Args:
            album_name: Album name.

        Returns:
            Album ID or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT album_id FROM music WHERE album_name=?", (album_name,)
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:
            return result[0]

        return None

    def get_id_for_artist(self, artist_name: str) -> Union[str, None]:
        """Fetches the ID for an artist.

        Args:
            artist_name: Artist name.

        Returns:
            Artist ID or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT artist_id FROM music WHERE artist_0=?", (artist_name,)
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:  # Tear down
            cursor.close()
            connection.close()

        if result:
            return result[0]
        return None

    def album_for_song(
        self, song_title: str
    ) -> Union[Tuple[str, str], Tuple[None, None]]:
        """Fetches the album, which contains a song.

        Returns None if the song is not found.

        Args:
            song_title: Song title.

        Returns:
            The tuple of album name and artist name or the tuple of None, None
            if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Return also the artist and the album for the song
            cursor.execute(
                "SELECT album_name, artist_0 FROM music WHERE track_name=?",
                (song_title,),
            )
            result = cursor.fetchone()

            if result:
                return result[0], result[1]

            # Try alternative spelling
            song_names = self.fetch_transformed_song_name(song_title)

            if song_names:
                cursor.execute(
                    "SELECT album_name, artist_0 FROM music WHERE track_name=?",
                    (song_names[0][0],),
                )
                result = cursor.fetchone()
                if result:
                    return result[0], result[1]

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None, None

        finally:
            cursor.close()
            connection.close()

        return None, None

    # ----- Functions for the Surface Dictionaries -----

    def fetch_transformed_artist_id(self, artist_name: str) -> Union[str, None]:
        """Fetches the transformed artist ID.

        It is used to find the artist in the database if the user
        misspells the artist name. It queries the surface dictionary for the
        artist name.

        Args:
            artist_name: Artist name.

        Returns:
            The artist id, if found, or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT artist_id FROM transformed_artists WHERE transformed_artist=?",
                (artist_name,),
            )
            result = cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:  # return the artist id
            return result[0]
        return None  # artist not found

    def fetch_transformed_song_ids(self, song_name: str) -> Union[List[str], None]:
        """Fetches the transformed song IDs.

        It is used to find the song data in the surface dictionary if the user
        misspells the song name. It queries the surface dictionary for the
        song name.

        Args:
            song_name: Song name.

        Returns:
            List of song IDs, if found, or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT track_id FROM transformed_tracks WHERE transformed_track=?",
                (song_name,),
            )
            results = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if results:
            return [result[0] for result in results]  # return the song ids

        return None

    def fetch_transformed_songs_by_artist(
        self, song_name: str, artist_name: str
    ) -> Union[List[Song], None]:
        """Fetches the songs by their alternative names.

        It helpes to find the song in the database if the user misspells the
        song name. It combines the fetch_transformed_artist_id and the
        fetch_transformed_song_ids methods.

        Args:
            song_name: Song name.
            artist_name: Artist name.

        Returns:
            List of song objects if found, otherwise None.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        # Convert the names to lowercase
        song_name = song_name.lower()
        artist_name = artist_name.lower()

        # Find the artist and the song ids in the surface dictionaries
        artist_id = self.fetch_transformed_artist_id(artist_name)
        song_ids = self.fetch_transformed_song_ids(song_name)

        if not artist_id or not song_ids:
            return None  # Song or artist not found

        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Prepare query
            query = f"""
                SELECT * FROM music WHERE track_id IN
                ({','.join(['?'] * len(song_ids))}) AND artist_id=?
            """
            cursor.execute(query, (*song_ids, artist_id))
            results = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if results:
            return [Song(*result) for result in results]
        return None

    def fetch_transformed_songs_by_title(
        self, song_title: str
    ) -> Union[List[Song], None]:
        """Fetches the songs by their alternative names.

        It uses only the name of the song to find the song in the database if
        the user misspells the song name. It queries the surface dictionary for
        the song name.
        """
        # Convert the name to lowercase
        song_title = song_title.lower()

        # Find the song ids in the surface dictionary
        song_ids = self.fetch_transformed_song_ids(song_title)

        if not song_ids:
            return None

        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Prepare query
            query = f"""
                SELECT * FROM music WHERE track_id IN
                ({','.join(['?'] * len(song_ids))})
            """
            cursor.execute(query, (*song_ids,))
            results = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if results:
            return [Song(*result) for result in results]
        return None

    def fetch_transformed_song_name(self, song_name: str) -> Union[List[str], None]:
        """Fetches the song name for a misspelled name.

        It is used in the delete method of the app.py file to delete a song.

        Args:
            song_name: Song name.

        Returns:
            List of transformed song names or None if not found.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        song_name = song_name.lower()

        # Setup
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT original_track FROM transformed_tracks WHERE transformed_track=?",
                (song_name,),
            )
            result = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

        if result:
            return result
        return None
