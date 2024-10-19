"""Module is used to convert a CSV file to a SQLite database.

We used it to initially create the database for the project.
"""

import sqlite3

import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("spotify_data_12_20_2023.csv")

    conn = sqlite3.connect("final_database.db")

    # Converting the DataFrame to a SQL table
    df.to_sql("music", conn, if_exists="replace", index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully!")
