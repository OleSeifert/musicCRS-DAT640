"""Creates a Flask app that fetches the songs from the playlist file.

The app has a single endpoint that returns the songs from the playlist file and
runs on port 5002.

To run execute the following command:

`python app.py`
"""

import os
from typing import List, Tuple, Union

from flask import Flask, jsonify, request
from flask_cors import CORS

from data import database_manager
from data import recommendations as rec
from models.playlist import Playlist
from models.song import Song
from nlu import mappings, post_processing

DB_PATH = os.path.abspath("data/final_database.db")

app = Flask(__name__)
CORS(app)

# Populate playlist initially with some songs
playlist = Playlist("My Playlist")
playlist.add_song(Song(track_name="I Won't Give Up", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="93 Million Miles", artist_0="Jason Mraz"))
playlist.add_song(Song(track_name="Let It Be", artist_0="The Beatles"))

suggestions = Playlist("Suggestions")
# suggestions.add_song(Song(track_name="Yesterday", artist_0="The Beatles"))
# suggestions.add_song(Song(track_name="Hey Jude", artist_0="The Beatles"))

recommendations = Playlist("Recommendations")
# recommendations.add_song(Song(track_name="Let It Be", artist_0="The Beatles"))


@app.route("/songs", methods=["GET"])
def get_songs():
    """Returns the playlist as strings, one for each song."""
    # Usa il metodo __str__ per ogni oggetto Song
    playlist_strings = [str(song) for song in playlist.songs]
    return jsonify(playlist_strings)


@app.route("/suggestions", methods=["GET"])
def get_suggestions():
    """Returns the suggestions as strings with an indication if they are in the playlist."""

    playlist_track_ids = {song.track_id for song in playlist.songs}

    suggestions_data = []
    for song in suggestions.songs:
        suggestion_entry = {
            "message": str(song),
            "disabled": song.track_id
            in playlist_track_ids,  # Disable the button if the song is in the playlist
        }
        suggestions_data.append(suggestion_entry)

    return jsonify(suggestions_data), 200


@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    """Returns the recommendations as strings with an indication if they are in
    the playlist.

    It is called from the `index.html` file to update the recommendations list.
    """

    playlist_track_ids = {song.track_id for song in playlist.songs}

    recommendations_data = []
    for song in recommendations.songs:
        recommendation_entry = {
            "message": str(song),
            "disabled": song.track_id
            in playlist_track_ids,  # Disable the button if the song is in the playlist
        }
        recommendations_data.append(recommendation_entry)

    return jsonify(recommendations_data), 200


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

    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format. Expected a list of songs."}), 400

    results = []
    suggestions.clear()  # clear suggestions

    for song_data in data:
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
        key=lambda song: (
            song.track_popularity if song.track_popularity is not None else 0
        ),
        reverse=True,
    )
    return jsonify(results), 201


@app.route("/create_playlist", methods=["POST"])
def create_entire_playlist():
    """Adds multiple songs to the playlist."""
    data = request.get_json()

    # Extract the parameters from the request
    valence = mappings.VALENCE_MAPPING[post_processing.extract_valence(data)]
    energy = mappings.ENERGY_MAPPING[post_processing.extract_energy(data)]
    danceability = mappings.DANCEABILITY_MAPPING[
        post_processing.extract_danceability(data)
    ]
    tempo = mappings.TEMPO_MAPPING[post_processing.extract_tempo(data)]
    genres = post_processing.extract_genres(data)
    duration = post_processing.extract_duration(data)

    # Query the database
    db_manager = database_manager.DatabaseManager(DB_PATH)
    playlist.clear()
    playlist.songs = db_manager.query_songs_for_playlist_generation(
        tempo, danceability, valence, energy, genres, duration
    )

    results = []
    return jsonify(results), 201


@app.route("/add_recommendations", methods=["GET"])
def add_recommendations():
    """Adds multiple songs to the recommendations list."""

    track_ids = [song.track_id for song in playlist.songs]
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/final_database.db")
    )

    # Get recommendations
    recommendation_ids = rec.get_recommendations(
        db_path=db_path, playlist_track_ids=track_ids
    )

    # Fetch song data from the database using track ids
    db_manager = database_manager.DatabaseManager(db_path)
    recommendation_songs = db_manager.fetch_songs_by_track_ids(recommendation_ids)

    results = []
    recommendations.clear()  # clear suggestions

    for song in recommendation_songs:
        result = recommendations.add_song(song)
        if result == -1:
            results.append(
                {
                    "error": f"'{song.track_name}' by {song.artist_0} is already in suggestions"
                }
            )
        else:
            results.append(
                {
                    "message": f"'{song.track_name}' by {song.artist_0} added to suggestions"
                }
            )
    # recommendations.songs.sort(
    #     key=lambda song: (
    #         song.track_popularity if song.track_popularity is not None else 0
    #     ),
    #     reverse=True,
    # )
    return jsonify(results), 201


@app.route("/delete_song", methods=["DELETE"])
def delete_song():
    """Delete a song from the playlist by track name."""
    data = request.get_json()
    track_name = data.get("track_name")

    if not track_name:
        return jsonify({"error": "track_name is required"}), 400

    result = playlist.remove_song(track_name)

    if result == -1:
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/final_database.db")
        )
        db_manager = database_manager.DatabaseManager(db_path)

        results_db = db_manager.fetch_transformed_song_name(track_name)

        if results_db is None:
            return jsonify({"error": "The song is not in the playlist"}), 401

        for song_name in results_db:
            result = playlist.remove_song(song_name[0])

            if result != -1:
                break

        if result == -1:  # Still not found
            return (jsonify({"error": "The song is not in the playlist"}), 401)

    return (
        jsonify({"message": f"'{track_name}' has been removed from the playlist"}),
        200,
    )


@app.route("/delete_songs_by_positions", methods=["DELETE"])
def delete_songs():
    """Delete songs from the playlist by positions."""
    data = request.get_json()
    positions = data.get("positions")

    if not positions:
        return jsonify({"error": "track_name is required"}), 400

    result = playlist.remove_songs_by_positions(positions)

    if result == -1:
        return (jsonify({"error": "These positions are not available"}), 401)

    return (
        jsonify(
            {
                "message": f"Songs in positions:'{positions}' has been removed from the playlist"
            }
        ),
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


def parse_song_string(song_str: str) -> Tuple[Union[str, None], List[str]]:
    """Parses a song string to extract the track name and artists.

    Args:
        song_str: String of the song with the format
          "<song_name> by <artist_name_1>, <artist_name_2>, ..."

    Returns:
        A tuple consisting of the track name and a list of artists. Or None if
        the song string is not in the correct format.
    """
    if " by " not in song_str:
        return None, []
    track_name, artists_str = song_str.split(" by ", 1)
    artists = [artist.strip() for artist in artists_str.split(",")]
    return track_name.strip(), artists


@app.route("/add_to_playlist", methods=["POST"])
def add_to_playlist():
    """Adds a song from the suggestions to the playlist."""
    data = request.get_json()
    song_str = data.get("song")

    track_name, artists = parse_song_string(song_str)

    if not track_name or not artists:
        return jsonify({"error": "Invalid song format"}), 400

    song = suggestions.find_song(track_name, artists)
    if song:
        suggestions.remove_song(track_name, artists)
        playlist.add_song(song)

        suggestions.songs.clear()

        return (
            jsonify({"message": "Song moved to playlist and suggestions cleared"}),
            200,
        )
    else:
        return jsonify({"error": "Song not found in suggestions"}), 404


@app.route("/add_recommendation_to_playlist", methods=["POST"])
def add_recommendation_to_playlist():
    """Adds songs in the recommendations to the playlist."""
    data = request.get_json()
    songs_data = data.get("songs")  # Lista di canzoni da aggiungere alla playlist

    if not songs_data:
        return jsonify({"error": "No songs provided"}), 400

    added_songs = []  # Lista per tracciare le canzoni aggiunte
    not_found_songs = []  # Lista per tracciare le canzoni non trovate

    for song_str in songs_data:
        track_name, artists = parse_song_string(song_str)

        if not track_name or not artists:
            not_found_songs.append(song_str)
            continue

        # Trova la canzone nelle raccomandazioni
        song = recommendations.find_song(track_name, artists)
        if song:
            recommendations.remove_song(track_name, artists)
            playlist.add_song(song)
            added_songs.append(song)
        else:
            not_found_songs.append(song_str)

    if added_songs:
        # Se almeno una canzone è stata aggiunta alla playlist
        response_message = f"{len(added_songs)} recommendations added to the playlist"
    else:
        # Se nessuna canzone è stata trovata o aggiunta
        response_message = "No valid songs found to add to the playlist"

    recommendations.clear()  # Clear the recommendations

    return (
        jsonify(
            {
                "message": response_message,
                "added_songs": [song.serialize() for song in added_songs],
                "not_found_songs": not_found_songs,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(port=5002)
