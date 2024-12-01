import os
import sqlite3
from typing import List

db_path = "data/final_database.db"  # Replace with your actual path
print("Database absolute path:", os.path.abspath(db_path))

# conn = sqlite3.connect("data/final_database.db")
# cursor = conn.cursor()

# find the number of unique transformed tracks
# cursor.execute(
#     """
#     SELECT original_artist, artist_id FROM transformed_artists WHERE transformed_artist='taylor swift'
# """
# )
# cursor.execute(
#     """
#     SELECT COUNT(DISTINCT album_id) FROM music WHERE artist_0='taylor swift'
# """
# )

# update beatles artist id
# cursor.execute(
#     """
#     UPDATE transformed_artists
#     SET artist_id='3WrFJ7ztbogyGnTHbHJFl2'
#     WHERE original_artist='The Beatles'
#     """
# )

# # results = cursor.fetchall()

# conn.commit()
# print("Beatles artist id updated successfully.")

# # print(f"Number of unique transformed artists: {type(results[0])}")

# # results = cursor.fetchone()
# conn.close()


def query_songs_for_playlist_generation(
    tempo_range: List[int],
    danceability_range: List[float],
    valence_range: List[float],
    energy_range: List[float],
    genres: List[str],
    num_songs: int = 10,
):
    """Queries db for songs to generate a playlist with specified features.

    Args:
        tempo_range: Range of tempo. From 0 to 250.
        danceability_range: Range of danceability. From 0.0 to 1.0.
        valence_range: Range of valence. From 0.0 to 1.0.
        energy_range: Range of energy. From 0.0 to 1.0.
        genres: List of genres. Possibly empty.
        num_songs: Number of songs to return. Defaults to 10.

    Returns:
        A list of song objects, that match the specified features.

    Raises:
        sqlite3.Error: If an error occurs while querying the database.
    """
    connection = sqlite3.connect(os.path.abspath(db_path))
    cursor = connection.cursor()

    try:
        # Start building the SQL query
        query = """
        SELECT * FROM music
        WHERE tempo BETWEEN ? AND ?
        AND danceability BETWEEN ? AND ?
        AND valence BETWEEN ? AND ?
        AND energy BETWEEN ? AND ?
        """
        params = [
            tempo_range[0],
            tempo_range[1],
            danceability_range[0],
            danceability_range[1],
            valence_range[0],
            valence_range[1],
            energy_range[0],
            energy_range[1],
        ]

        # Add genre filtering
        if genres:
            genre_conditions = []
            for genre in genres:
                genre_conditions.append("genre_0 LIKE ?")
                params.append(f"%{genre}%")
            query += f" AND ({' OR '.join(genre_conditions)})"

        # Sort by popularity and limit the number of results
        query += " ORDER BY track_popularity DESC LIMIT ?"
        params.append(num_songs)

        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        connection.close()

    return results


def print_column_titles_and_types(db_name, table_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to get column names and their types
    query = f"PRAGMA table_info({table_name});"
    cursor.execute(query)

    # Fetch all results
    columns = cursor.fetchall()

    # Print column names and types
    print(f"Columns in '{table_name}':")
    for column in columns:
        column_name = column[1]
        column_type = column[2]
        print(f"Column: {column_name}, Type: {column_type}")

    # Close the connection
    conn.close()


def get_genres():
    connection = sqlite3.connect(os.path.abspath(db_path))
    cursor = connection.cursor()

    try:
        # Start building the SQL query
        query = """
        SELECT genre_0, COUNT(*) as frequency
        FROM music
        GROUP BY genre_0
        ORDER BY frequency DESC
        LIMIT 20;
        """
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        connection.close()

    return results


def query_null_values_duration():
    connection = sqlite3.connect(os.path.abspath(db_path))
    cursor = connection.cursor()

    try:
        # Start building the SQL query
        query = """
        SELECT COUNT(*) AS null_count
        FROM music
        WHERE duration_sec IS NULL;
        """
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        connection.close()

    return results


# Usage
database_name = "data/final_database.db"  # Replace with your database name
# table_name = "music"  # Replace with your table name
# print(
#     query_songs_for_playlist_generation(
#         tempo_range=[0, 100],
#         danceability_range=[0.0, 0.33],
#         valence_range=[0.33, 0.66],
#         energy_range=[0, 0.33],
#         genres=["folk", "indie", "acoustic"],
#         num_songs=10,
#     )
# )
# print_column_titles_and_types(os.path.abspath(db_path), table_name)
print(query_null_values_duration())
