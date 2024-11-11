"""This module contains the functions that are used to generate recommadations.

The recommendations are generated based on the current playlist.
"""

import sqlite3
from typing import List

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


def get_cached_neighbors(db_path: str, track_id: str) -> List[str]:
    """Retrieves cached similar tracks for a given track ID.

    Args:
        db_path: Path to the database.
        track_id: The track ID for which to retrieve neighbors.

    Returns:
        A list of similar track IDs. If no neighbors are cached, an empty list
        is returned.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT similar_tracks FROM similar_songs WHERE track_id = ?", (track_id,)
    )
    result = cursor.fetchone()
    connection.close()
    return result[0].split(",") if result else []


def compute_and_store_neighbors(
    db_path: str, track_id: str, all_features: pd.DataFrame, top_n: int = 10
) -> List[str]:
    """Computes and stores the top N neighbors for a specific track ID.

    Args:
        db_path: Path to the database.
        track_id: The track ID for which to compute neighbors.
        all_features: DataFrame containing all song features.
        top_n (optional): Number of neighbors to return. Defaults to 10.

    Returns:
        A list of the top N similar track IDs.
    """
    # Extract features for all songs
    track_ids = all_features["track_id"].values
    features = all_features.drop(columns=["track_id"])

    # Normalize features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Find the index of the track_id in the features dataset
    song_idx = all_features[all_features["track_id"] == track_id].index[0]

    # Compute cosine similarity for this song against all others
    similarity_scores = cosine_similarity(
        features[song_idx].reshape(1, -1), features
    ).flatten()
    similar_indices = similarity_scores.argsort()[-(top_n + 1) : -1][
        ::-1
    ]  # Top N neighbors excluding itself
    similar_track_ids = [track_ids[i] for i in similar_indices if i != song_idx]

    # Cache the result in the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    similar_tracks_str = ",".join(similar_track_ids)
    cursor.execute(
        """INSERT OR REPLACE INTO similar_songs (track_id, similar_tracks)
           VALUES (?, ?)""",
        (track_id, similar_tracks_str),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return similar_track_ids


def get_recommendations(
    db_path: str, playlist_track_ids: List[str], top_n: int = 10
) -> List[str]:
    """Generates ranked recommendations based on the current playlist.

    Args:
        db_path: Path to the database.
        playlist_track_ids: The track IDs in the current playlist.
        top_n (optional): Number of recommendations to retrieve. Defaults to
          10.

    Returns:
        A list of the top N recommended track IDs. Ranked based on how often
        songs have the same neighbors, or the popularity of the song.
    """
    all_features = fetch_all_song_features(db_path)
    all_recommendations = []

    # For each track in the playlist, fetch or compute similar tracks
    for track_id in playlist_track_ids:
        similar_tracks = get_cached_neighbors(db_path, track_id)
        if not similar_tracks:  # If not cached, compute and store
            similar_tracks = compute_and_store_neighbors(
                db_path, track_id, all_features, top_n
            )
        all_recommendations.extend(similar_tracks)

    # Count occurrences of each recommendation
    recommendation_counts = pd.Series(all_recommendations).value_counts()

    # Load track popularity for sorting
    connection = sqlite3.connect(db_path)
    popularity_query = (
        "SELECT track_id, track_popularity FROM music WHERE track_id IN ({})"
    )
    format_strings = ",".join(["?"] * len(recommendation_counts.index))
    popularity_data = pd.read_sql(
        popularity_query.format(format_strings),
        connection,
        params=recommendation_counts.index.tolist(),
    )
    connection.close()

    # Merge counts and popularity for sorting
    popularity_df = popularity_data.set_index("track_id").reindex(
        recommendation_counts.index
    )
    popularity_df["count"] = recommendation_counts.values

    # Sort first by count (descending), then by track popularity (descending)
    popularity_df.sort_values(
        by=["count", "track_popularity"], ascending=[False, False], inplace=True
    )

    return popularity_df.index[:top_n].tolist()
