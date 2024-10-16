"""Creates a Flask app that fetches the songs from the playlist file.

The app has a single endpoint that returns the songs from the playlist file and
runs on port 5002.

To run execute the following command:

`python app.py`
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from models.playlist import Playlist
from models.song import Song
app = Flask(__name__)
CORS(app)

playlist = Playlist("My Playlist")
playlist.add_song(Song("I Won't Give Up", "Jason Mraz"))
playlist.add_song(Song("93 Million Miles", "Jason Mraz"))
playlist.add_song(Song("Let It Be", "The Beatles"))

@app.route("/songs", methods=["GET"])
def get_songs():
    """Restituisce la playlist come stringhe, una per ogni canzone."""
    # Usa il metodo __str__ per ogni oggetto Song
    playlist_strings = [str(song) for song in playlist.songs]
    return jsonify(playlist_strings)



if __name__ == "__main__":
    app.run(port=5002)
