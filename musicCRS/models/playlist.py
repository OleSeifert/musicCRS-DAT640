"""Module for the Playlist class."""

from musicCRS.models.song import Song


class Playlist:
    """Class to represent a playlist of songs.

    Attributes:
        name (str): The name of the playlist.
        songs (list): A list of Song objects in the playlist.
    """

    def __init__(self, name: str) -> None:
        """Initialize the playlist with a name and an empty list of songs."""
        self.name = name
        self.songs = []

    def add_song(self, song: Song) -> int:
        """Adds a song to the playlist.

        Args:
            song: The Song object to add to the playlist.

        Returns:
            An integer representing the status of the operation:
            0: The song was successfully added to the playlist.
            -1: The song is already in the playlist.
            -2: The input is not a Song object.
        """
        if isinstance(song, Song):
            if song in self.songs:
                print(
                    f"'{song.track_name}' by {song.artist_0} is already in the playlist."
                )
                return -1
            self.songs.append(song)
            print(f"Added '{song.track_name}' by {song.artist_0} to the playlist.")
            return 0
        else:
            print("Error: Only Song objects can be added.")
            return -2

    def remove_song(self, track_name: str, artists: list = None) -> int:
        """Removes a song from the playlist.

        Args:
            track_name: The name of the track to remove from the playlist.
            artists: An optional list of artist names to match when removing.

        Returns:
            An integer representing the status of the operation:
            0: The song was successfully removed from the playlist.
            -1: The song was not found in the playlist.
        """
        for song in self.songs:
            # Controlla se il nome della traccia coincide
            if song.track_name == track_name:
                if artists is None:
                    # Rimuove la canzone basandosi solo sul nome della traccia se gli artisti non sono specificati
                    self.songs.remove(song)
                    print(f"Removed '{track_name}' from the playlist.")
                    return 0
                else:
                    # Controllo opzionale degli artisti se specificati
                    song_artists = [
                        song.artist_0,
                        song.artist_1,
                        song.artist_2,
                        song.artist_3,
                        song.artist_4,
                    ]
                    song_artists = [
                        artist for artist in song_artists if artist
                    ]  # Rimuove valori None

                    if song_artists == artists:
                        # Rimuove la canzone solo se sia il nome della traccia sia gli artisti corrispondono
                        self.songs.remove(song)
                        print(
                            f"Removed '{track_name}' by {', '.join(artists)} from the playlist."
                        )
                        return 0
        return -1

    # remove songs by positions
    def remove_songs_by_positions(self, positions: list) -> int:
        """Removes songs from the playlist based on their positions.

        Args:
            positions: A list of integers representing the positions of the songs to remove.

        Returns:
            An integer representing the status of the operation:
            0: The songs were successfully removed from the playlist.
            -1: None of the positions were found in the playlist.
        """

        if any(pos < 0 or pos >= len(self.songs) for pos in positions):
            print("Error: Some positions are out of range.")
            return -1

        for pos in sorted(positions, reverse=True):
            song = self.songs.pop(pos)
            print(f"Removed '{song.track_name}' from the playlist.")

        return 0

    def find_song(self, track_name: str, artists: list = None) -> Song:
        """Finds a song in the playlist based on track name and optionally artists.

        Args:
            track_name: The name of the track to find.
            artists: An optional list of artist names to match.

        Returns:
            The Song object if found, otherwise None.
        """
        for song in self.songs:
            # Controlla il nome della traccia
            if song.track_name == track_name:
                # Se gli artisti sono specificati, verifica che coincidano
                song_artists = [
                    song.artist_0,
                    song.artist_1,
                    song.artist_2,
                    song.artist_3,
                    song.artist_4,
                ]
                song_artists = [artist for artist in song_artists if artist]

                if artists is None or song_artists == artists:
                    return song  # Restituisce l'oggetto Song trovato
        return None

    def __str__(self) -> str:
        """Returns a string representation of the playlist with all songs."""
        playlist_str = f"Playlist: {self.name}\n"
        playlist_str += "\n".join(
            [
                f"{idx + 1}. {song.track_name} by {song.artist_0}"
                for idx, song in enumerate(self.songs)
            ]
        )
        return playlist_str if self.songs else f"Playlist: {self.name} (empty)"

    def clear(self) -> None:
        """Removes all songs from the playlist."""
        self.songs = []
        print("All songs have been removed from the playlist.")
