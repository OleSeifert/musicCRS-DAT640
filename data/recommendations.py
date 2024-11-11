"""This module contains the functions that are used to generate recommadations.

The recommendations are generated based on the current playlist.
"""

import sqlite3
from typing import List

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler







def get_playlist_recommendations(
    db_path: str, playlist_track_ids: List[str], top_n: int = 10
) -> List[str]:
    """Fetches recommendations based on the playlist.

    Args:
        db_path: Path to the database.
        playlist_track_ids: List of track IDs in the playlist.
        top_n (optional): Number of recommendations to return. Defaults to 10.

    Returns:
        List of recommended track IDs.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    recommendations = []
    for track_id in playlist_track_ids:
        cursor.execute(
            "SELECT similar_tracks FROM similar_songs WHERE track_id = ?", (track_id,)
        )
        result = cursor.fetchone()
        if result:
            similar_tracks = result[0].split(",")
            recommendations.extend(similar_tracks)

    # Close the database connection
    cursor.close()
    connection.close()

    # Rank recommendations by frequency (most common similar tracks across playlist songs)
    # TODO: Improve recommendation ranking
    #  Use popularity of the tracks as fallback if no songs appear multiple times

    recommendations = pd.Series(recommendations).value_counts().index.tolist()
    return recommendations[:top_n]


# TODO: Needs to deal with NULL values in the database
