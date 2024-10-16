from models.song import Song
class Playlist:
    def __init__(self, name):
        # Inizializza la playlist con un nome e una lista vuota di canzoni
        self.name = name
        self.songs = []

    def add_song(self, song):
        # Aggiungi una canzone alla playlist
        if isinstance(song, Song):
            self.songs.append(song)
            print(f"Added '{song.track_name}' by {song.artist_0} to the playlist.")
        else:
            print("Error: Only Song objects can be added.")

    def remove_song(self, track_name):
        # Rimuovi una canzone dalla playlist cercandola per nome traccia
        for song in self.songs:
            if song.track_name == track_name:
                self.songs.remove(song)
                print(f"Removed '{track_name}' from the playlist.")
                return
        print(f"Song '{track_name}' not found in the playlist.")

    def __str__(self):
        # Restituisce una rappresentazione in stringa della playlist con tutte le canzoni
        playlist_str = f"Playlist: {self.name}\n"
        playlist_str += "\n".join([f"{idx + 1}. {song.track_name} by {song.artist_0}" for idx, song in enumerate(self.songs)])
        return playlist_str if self.songs else f"Playlist: {self.name} (empty)"