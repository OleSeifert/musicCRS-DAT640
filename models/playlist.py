"""Module for the Playlist class."""

from models.song import Song


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

    def remove_song(self, track_name: str) -> int:
        """Removes a song from the playlist.

        Args:
            track_name: The name of the track to remove from the playlist.

        Returns:
            An integer representing the status of the operation:
            0: The song was successfully removed from the playlist.
            -1: The song was not found in the playlist.
        """
        # Remove a song from the playlist by searching for it by track name
        for song in self.songs:
            if song.track_name == track_name:
                self.songs.remove(song)
                print(f"Removed '{track_name}' from the playlist.")
                return 0
        return -1

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
