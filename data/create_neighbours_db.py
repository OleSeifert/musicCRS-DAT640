import sqlite3

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


def fetch_all_song_features(db_path: str) -> pd.DataFrame:
    """Fetches all song features from the database."""
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


def compute_and_store_neighbors_one_by_one(db_path: str, top_n: int = 10) -> None:
    """Computes and stores the top N neighbors for each song one at a time."""
    # Fetch features for all songs and normalize
    all_songs = fetch_all_song_features(db_path)
    track_ids = all_songs["track_id"].values
    features = all_songs.drop(columns=["track_id"])

    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Connect to the database
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

    # Compute neighbors for each song individually
    for idx, track_id in enumerate(track_ids):
        # Compute cosine similarity between this song and all others
        similarity_scores = cosine_similarity(
            features[idx].reshape(1, -1), features
        ).flatten()

        # Get indices of the top N most similar songs (excluding the song itself)
        similar_indices = similarity_scores.argsort()[-(top_n + 1) : -1][::-1]
        similar_track_ids = [track_ids[i] for i in similar_indices if i != idx]

        # Store results in database as a comma-separated string
        similar_tracks_str = ",".join(similar_track_ids[:top_n])
        cursor.execute(
            """INSERT OR REPLACE INTO similar_songs (track_id, similar_tracks)
               VALUES (?, ?)""",
            (track_id, similar_tracks_str),
        )

        # Print progress
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1} of {len(track_ids)} songs.")

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
    print("All neighbors computed and stored successfully.")


# Run the function
db_path = "final_database.db"  # Update with the actual path to your database
compute_and_store_neighbors_one_by_one(db_path, top_n=10)
