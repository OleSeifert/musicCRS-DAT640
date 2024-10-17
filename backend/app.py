"""Creates a Flask app that fetches the songs from the playlist file.

The app has a single endpoint that returns the songs from the playlist file and
runs on port 5002.

To run execute the following command:

`python app.py`
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.playlist import Playlist
from models.song import Song
app = Flask(__name__)
CORS(app)

playlist = Playlist("My Playlist")
playlist.add_song(Song(track_name="I Won't Give Up", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="93 Million Miles", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="Let It Be", artist_0="The Beatles"))

@app.route("/songs", methods=["GET"])
def get_songs():
    """Restituisce la playlist come stringhe, una per ogni canzone."""
    # Usa il metodo __str__ per ogni oggetto Song
    playlist_strings = [str(song) for song in playlist.songs]
    return jsonify(playlist_strings)


@app.route("/add_song", methods=["POST"])
def add_song():
    """Aggiunge una nuova canzone alla playlist."""
    data = request.get_json()

    # Estraiamo tutti i campi dalla richiesta JSON
    new_song = Song(
        album_id=data.get('album_id'),
        album_name=data.get('album_name'),
        album_popularity=data.get('album_popularity'),
        album_type=data.get('album_type'),
        artists=data.get('artists'),
        artist_0=data.get('artist_0'),
        artist_1=data.get('artist_1'),
        artist_2=data.get('artist_2'),
        artist_3=data.get('artist_3'),
        artist_4=data.get('artist_4'),
        artist_id=data.get('artist_id'),
        duration_sec=data.get('duration_sec'),
        label=data.get('label'),
        release_date=data.get('release_date'),
        total_tracks=data.get('total_tracks'),
        track_id=data.get('track_id'),
        track_name=data.get('track_name'),
        track_number=data.get('track_number'),
        artist_genres=data.get('artist_genres'),
        artist_popularity=data.get('artist_popularity'),
        followers=data.get('followers'),
        name=data.get('name'),
        genre_0=data.get('genre_0'),
        genre_1=data.get('genre_1'),
        genre_2=data.get('genre_2'),
        genre_3=data.get('genre_3'),
        genre_4=data.get('genre_4'),
        acousticness=data.get('acousticness'),
        analysis_url=data.get('analysis_url'),
        danceability=data.get('danceability'),
        duration_ms=data.get('duration_ms'),
        energy=data.get('energy'),
        instrumentalness=data.get('instrumentalness'),
        key=data.get('key'),
        liveness=data.get('liveness'),
        loudness=data.get('loudness'),
        mode=data.get('mode'),
        speechiness=data.get('speechiness'),
        tempo=data.get('tempo'),
        time_signature=data.get('time_signature'),
        track_href=data.get('track_href'),
        track_type=data.get('track_type'),
        uri=data.get('uri'),
        valence=data.get('valence'),
        explicit=data.get('explicit'),
        track_popularity=data.get('track_popularity'),
        release_year=data.get('release_year'),
        release_month=data.get('release_month'),
        rn=data.get('rn')
    )

    # Aggiungiamo la canzone alla playlist
    result = playlist.add_song(new_song)
    if result == -1:
        return jsonify({"error": f"'{data.get('track_name')}' by {data.get('artist_0')} is already in the playlist"}), 401
    return jsonify({"message": f"'{data.get('track_name')}' by {data.get('artist_0')} added to the playlist"}), 201

@app.route("/delete_song", methods=["DELETE"])
def delete_song():
    """Cancella una canzone dalla playlist per nome della traccia."""
    data = request.get_json()
    track_name = data.get('track_name')

    # Verifica se track_name è stato fornito
    if not track_name:
        return jsonify({"error": "track_name is required"}), 400


    # Rimuove la canzone dalla playlist
    result = playlist.remove_song(track_name)

    if result == -1:
        return jsonify({"error": "The song is not in the playlist"}), 401


    return jsonify({"message": f"'{track_name}' has been removed from the playlist"}), 200

@app.route("/songs_string", methods=["GET"])
def get_songs_as_string():
    """Restituisce tutte le canzoni in una singola stringa, separate da un delimitatore."""
    # Usa il metodo __str__ per ogni oggetto Song e uniscile in una singola stringa
    songs_string = "//".join([str(song) for song in playlist.songs])
    return songs_string, 200


@app.route("/clear_playlist", methods=["DELETE"])
def clear_playlist():
    """Cancella tutte le canzoni dalla playlist."""
    playlist.clear()  # Pulisce la lista delle canzoni
    return jsonify({"message": "All songs have been removed from the playlist"}), 200

@app.route('/getSuggestions', methods=['GET'])
def get_suggestions():
    suggestions = ["Play music", "Create playlist", "Show recommendations"]
    return jsonify({"suggestions": suggestions})



if __name__ == "__main__":
    app.run(port=5002)
