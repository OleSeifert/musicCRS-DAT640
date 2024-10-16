"""Contains the DatabaseManager class."""

import datetime
import sqlite3
from typing import Union
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
                    "SELECT * FROM music WHERE track_name=? AND artist_0 = ?",
                    (song_title, artist),
                )
                results = cursor.fetchall()
                if not results:
                    cursor.execute(
                        "SELECT * FROM music WHERE track_name=? AND artists LIKE ?",
                        (song_title, f"%{artist}%"),
                    )
                    results = cursor.fetchall()
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
            total_results = len(results)
            # Take the first result from the list and create a Song object
            first_result = results[0]
            song = Song(
                album_id=first_result[0],
                album_name=first_result[1],
                album_popularity=first_result[2],
                album_type=first_result[3],
                artists=first_result[4],
                artist_0=first_result[5],
                artist_1=first_result[6],
                artist_2=first_result[7],
                artist_3=first_result[8],
                artist_4=first_result[9],
                artist_id=first_result[10],
                duration_sec=first_result[11],
                label=first_result[12],
                release_date=first_result[13],
                total_tracks=first_result[14],
                track_id=first_result[15],
                track_name=first_result[16],
                track_number=first_result[17],
                artist_genres=first_result[18],
                artist_popularity=first_result[19],
                followers=first_result[20],
                name=first_result[21],
                genre_0=first_result[22],
                genre_1=first_result[23],
                genre_2=first_result[24],
                genre_3=first_result[25],
                genre_4=first_result[26],
                acousticness=first_result[27],
                analysis_url=first_result[28],
                danceability=first_result[29],
                duration_ms=first_result[30],
                energy=first_result[31],
                instrumentalness=first_result[32],
                key=first_result[33],
                liveness=first_result[34],
                loudness=first_result[35],
                mode=first_result[36],
                speechiness=first_result[37],
                tempo=first_result[38],
                time_signature=first_result[39],
                track_href=first_result[40],
                track_type=first_result[41],
                uri=first_result[42],
                valence=first_result[43],
                explicit=first_result[44],
                track_popularity=first_result[45],
                release_year=first_result[46],
                release_month=first_result[47],
                rn=first_result[48]
            )
            return song, total_results
        else:
            return None, None

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
