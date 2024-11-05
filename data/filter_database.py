import sqlite3


def remove_duplicates():
    # Connect to the SQLite database
    conn = sqlite3.connect("final_database.db")
    cursor = conn.cursor()

    # Execute the query to delete duplicates
    cursor.execute("""
            DELETE FROM transformed_tracks
            WHERE ROWID IN (
                SELECT ROWID
                FROM (
                    SELECT ROWID,
                           ROW_NUMBER() OVER (PARTITION BY track_id, original_track, transformed_track ORDER BY ROWID) AS rn
                    FROM transformed_tracks
                ) t
                WHERE t.rn > 1
            )
        """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Duplicates removed successfully.")


# Example usage
remove_duplicates()
