"""Creates a Flask app that fetches the songs from the playlist file.

The app has a single endpoint that returns the songs from the playlist file and
runs on port 5002.

To run execute the following command:

`python app.py`
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from models.playlist import Playlist
from models.song import Song

app = Flask(__name__)
CORS(app)

# Populate playlist initially with some songs
playlist = Playlist("My Playlist")
playlist.add_song(Song(track_name="I Won't Give Up", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="93 Million Miles", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="Let It Be", artist_0="The Beatles"))

suggestions = Playlist("Suggestions")
suggestions.add_song(Song(track_name="Yesterday", artist_0="The Beatles"))
suggestions.add_song(Song(track_name="Hey Jude", artist_0="The Beatles"))

@app.route("/songs", methods=["GET"])
def get_songs():
    """Returns the playlist as strings, one for each song."""
    # Usa il metodo __str__ per ogni oggetto Song
    playlist_strings = [str(song) for song in playlist.songs]
    return jsonify(playlist_strings)

@app.route("/suggestions", methods=["GET"])
def get_suggestions():
    """Returns the suggestion as strings, one for each song."""
    # Usa il metodo __str__ per ogni oggetto Song
    suggestions_strings = [str(song) for song in suggestions.songs]
    return jsonify(suggestions_strings)


@app.route("/add_song", methods=["POST"])
def add_song():
    """Adds a new song to the playlist."""
    data = request.get_json()

    # Extract song data from the request
    new_song = Song(
        album_id=data.get("album_id"),
        album_name=data.get("album_name"),
        album_popularity=data.get("album_popularity"),
        album_type=data.get("album_type"),
        artists=data.get("artists"),
        artist_0=data.get("artist_0"),
        artist_1=data.get("artist_1"),
        artist_2=data.get("artist_2"),
        artist_3=data.get("artist_3"),
        artist_4=data.get("artist_4"),
        artist_id=data.get("artist_id"),
        duration_sec=data.get("duration_sec"),
        label=data.get("label"),
        release_date=data.get("release_date"),
        total_tracks=data.get("total_tracks"),
        track_id=data.get("track_id"),
        track_name=data.get("track_name"),
        track_number=data.get("track_number"),
        artist_genres=data.get("artist_genres"),
        artist_popularity=data.get("artist_popularity"),
        followers=data.get("followers"),
        name=data.get("name"),
        genre_0=data.get("genre_0"),
        genre_1=data.get("genre_1"),
        genre_2=data.get("genre_2"),
        genre_3=data.get("genre_3"),
        genre_4=data.get("genre_4"),
        acousticness=data.get("acousticness"),
        analysis_url=data.get("analysis_url"),
        danceability=data.get("danceability"),
        duration_ms=data.get("duration_ms"),
        energy=data.get("energy"),
        instrumentalness=data.get("instrumentalness"),
        key=data.get("key"),
        liveness=data.get("liveness"),
        loudness=data.get("loudness"),
        mode=data.get("mode"),
        speechiness=data.get("speechiness"),
        tempo=data.get("tempo"),
        time_signature=data.get("time_signature"),
        track_href=data.get("track_href"),
        track_type=data.get("track_type"),
        uri=data.get("uri"),
        valence=data.get("valence"),
        explicit=data.get("explicit"),
        track_popularity=data.get("track_popularity"),
        release_year=data.get("release_year"),
        release_month=data.get("release_month"),
        rn=data.get("rn"),
    )

    # Add the song to the playlist
    result = playlist.add_song(new_song)
    if result == -1:
        return (
            jsonify(
                {
                    "error": f"'{data.get('track_name')}' by {data.get('artist_0')} is already in the playlist"
                }
            ),
            401,
        )
    return (
        jsonify(
            {
                "message": f"'{data.get('track_name')}' by {data.get('artist_0')} added to the playlist"
            }
        ),
        201,
    )


@app.route("/add_suggestions", methods=["POST"])
def add_suggestions():
    """Adds multiple songs to the suggestions list."""
    data = request.get_json()

    # Verifica che i dati siano una lista di canzoni
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format. Expected a list of songs."}), 400

    # Lista per i risultati dell'aggiunta
    results = []

    for song_data in data:
        # Crea un oggetto Song per ogni canzone nella lista
        new_song = Song(
            album_id=song_data.get("album_id"),
            album_name=song_data.get("album_name"),
            album_popularity=song_data.get("album_popularity"),
            album_type=song_data.get("album_type"),
            artists=song_data.get("artists"),
            artist_0=song_data.get("artist_0"),
            artist_1=song_data.get("artist_1"),
            artist_2=song_data.get("artist_2"),
            artist_3=song_data.get("artist_3"),
            artist_4=song_data.get("artist_4"),
            artist_id=song_data.get("artist_id"),
            duration_sec=song_data.get("duration_sec"),
            label=song_data.get("label"),
            release_date=song_data.get("release_date"),
            total_tracks=song_data.get("total_tracks"),
            track_id=song_data.get("track_id"),
            track_name=song_data.get("track_name"),
            track_number=song_data.get("track_number"),
            artist_genres=song_data.get("artist_genres"),
            artist_popularity=song_data.get("artist_popularity"),
            followers=song_data.get("followers"),
            name=song_data.get("name"),
            genre_0=song_data.get("genre_0"),
            genre_1=song_data.get("genre_1"),
            genre_2=song_data.get("genre_2"),
            genre_3=song_data.get("genre_3"),
            genre_4=song_data.get("genre_4"),
            acousticness=song_data.get("acousticness"),
            analysis_url=song_data.get("analysis_url"),
            danceability=song_data.get("danceability"),
            duration_ms=song_data.get("duration_ms"),
            energy=song_data.get("energy"),
            instrumentalness=song_data.get("instrumentalness"),
            key=song_data.get("key"),
            liveness=song_data.get("liveness"),
            loudness=song_data.get("loudness"),
            mode=song_data.get("mode"),
            speechiness=song_data.get("speechiness"),
            tempo=song_data.get("tempo"),
            time_signature=song_data.get("time_signature"),
            track_href=song_data.get("track_href"),
            track_type=song_data.get("track_type"),
            uri=song_data.get("uri"),
            valence=song_data.get("valence"),
            explicit=song_data.get("explicit"),
            track_popularity=song_data.get("track_popularity"),
            release_year=song_data.get("release_year"),
            release_month=song_data.get("release_month"),
            rn=song_data.get("rn"),
        )

        # Aggiunge la canzone ai suggerimenti
        result = suggestions.add_song(new_song)
        if result == -1:
            results.append(
                {
                    "error": f"'{song_data.get('track_name')}' by {song_data.get('artist_0')} is already in suggestions"
                }
            )
        else:
            results.append(
                {
                    "message": f"'{song_data.get('track_name')}' by {song_data.get('artist_0')} added to suggestions"
                }
            )
    suggestions.songs.sort(
        key=lambda song: song.track_popularity if song.track_popularity is not None else 0,
        reverse=True
    )
    return jsonify(results), 201


@app.route("/delete_song", methods=["DELETE"])
def delete_song():
    """Delete a song from the playlist by track name."""
    data = request.get_json()
    track_name = data.get("track_name")

    # Verify that the track_name is provided
    if not track_name:
        return jsonify({"error": "track_name is required"}), 400

    # Remove the song from the playlist
    result = playlist.remove_song(track_name)

    if result == -1:
        return jsonify({"error": "The song is not in the playlist"}), 401

    return (
        jsonify({"message": f"'{track_name}' has been removed from the playlist"}),
        200,
    )


@app.route("/songs_string", methods=["GET"])
def get_songs_as_string():
    """Returns all songs in a single string, separated by a delimiter."""
    # Uses the __str__ method for each Song object
    songs_string = " // ".join([str(song) for song in playlist.songs])
    return songs_string, 200


@app.route("/clear_playlist", methods=["DELETE"])
def clear_playlist():
    """Delete all songs from the playlist."""
    playlist.clear()  # Clear the playlist
    return jsonify({"message": "All songs have been removed from the playlist"}), 200

def parse_song_string(song_str):
    if " by " not in song_str:
        return None, []
    track_name, artists_str = song_str.split(" by ", 1)
    artists = [artist.strip() for artist in artists_str.split(",")]
    return track_name.strip(), artists

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    data = request.get_json()
    song_str = data.get('song')

    # Decode the song string into track name and artists
    track_name, artists = parse_song_string(song_str)

    if not track_name or not artists:
        return jsonify({"error": "Invalid song format"}), 400

    # Trova la canzone nei suggerimenti
    song = suggestions.find_song(track_name, artists)
    if song:
        # Rimuove la canzone dai suggerimenti e la aggiunge alla playlist
        suggestions.remove_song(track_name, artists)
        playlist.add_song(song)

        # Svuota i suggerimenti
        suggestions.songs.clear()

        return jsonify({"message": "Song moved to playlist and suggestions cleared"}), 200
    else:
        return jsonify({"error": "Song not found in suggestions"}), 404

if __name__ == "__main__":
    app.run(port=5002)
