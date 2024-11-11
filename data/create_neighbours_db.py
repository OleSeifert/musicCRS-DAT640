import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def fetch_all_song_features(db_path: str) -> pd.DataFrame:
    """Fetches all song features from the DB.

    Args:
        db_path: The path to the database.

    Returns:
        A DataFrame containing all song features.
    """
    connection = sqlite3.connect(db_path)
    query = """
    SELECT track_id, danceability, energy, valence, acousticness,
        instrumentalness, liveness, speechiness, tempo, loudness,
        track_popularity, artist_popularity, album_popularity
    FROM music;
    """
    all_features = pd.read_sql(query, connection)
    connection.close()
    return all_features

def compute_and_store_similar_songs(db_path: str, top_n: int = 10) -> None:
    """Compute and store similar songs in the database.

    These are computed for every song in the database.

    Args:
        db_path: Path to the database.
        top_n (optional): Number of similar songs computed for each song.
          Defaults to 10.
    """
    # Fetch features for all songs
    all_songs = fetch_all_song_features(db_path)

    # Separate track IDs and feature values
    track_ids = all_songs["track_id"]
    features = all_songs.drop(columns=["track_id"])

    # Normalize features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(features)

    # Connect to database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Ensure similar_songs table exists
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS similar_songs (
        track_id TEXT PRIMARY KEY,
        similar_tracks TEXT
    )
    """
    )

    # Compute top N similar songs for each song
    for idx, track_id in enumerate(track_ids):
        # Get similarity scores for the current song
        similarity_scores = similarity_matrix[idx]

        # Get indices of the top N most similar songs (excluding the song itself)
        similar_indices = similarity_scores.argsort()[-(top_n + 1) : -1][::-1]
        similar_track_ids = track_ids.iloc[similar_indices].tolist()

        # Store in database as comma-separated string
        similar_tracks_str = ",".join(similar_track_ids)
        cursor.execute(
            """INSERT OR REPLACE INTO similar_songs (track_id, similar_tracks)
                VALUES (?, ?)""",
            (track_id, similar_tracks_str),
        )

    # Commit and close connection
    connection.commit()
    cursor.close()
    connection.close()
    print("Similarity data stored successfully.")


compute_and_store_similar_songs("final_database.db", 10)
