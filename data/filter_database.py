import sqlite3


def remove_duplicates():
    # Connect to the SQLite database
    conn = sqlite3.connect("final_database.db")
    cursor = conn.cursor()

    # Execute the query to delete duplicates
    cursor.execute(
        """
        DELETE FROM transformed_tracks
        WHERE ROWID NOT IN (
            SELECT MIN(ROWID)
            FROM transformed_tracks
            GROUP BY original_track, transformed_track
        )
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Duplicates removed successfully.")


# Example usage
remove_duplicates()
