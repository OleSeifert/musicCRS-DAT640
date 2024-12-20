import sqlite3
import pandas as pd
import re


def lower_case(string):
    return string.lower()


def remove_punctuation(string):
    return string.replace("'", "").replace(",", "").replace(".", "").replace('"', "")


def lower_case_remove_punctuation(string):
    return lower_case(remove_punctuation(string))


# delete everithing inside parenthesises
def remove_parentheses(title):
    # Check if the title is fully enclosed in a single pair of parentheses
    if title.startswith("(") and title.endswith(")"):
        return title[1:-1]  # Remove only the surrounding parentheses

    # Otherwise, remove all content within any parentheses
    return re.sub(r"\(.*?\)", "", title).strip()


def remove_after_separator(title):
    if " - " in title:
        return title.split(" - ")[0]
    return title


# remove 'the' if is at the start of the string
def remove_the(title):
    if title.lower().startswith("the "):
        return title[4:]
    return title


conn_original = sqlite3.connect("final_database.db")
query = "SELECT artist_id, artist_0 FROM music"


df = pd.read_sql_query(query, conn_original)

data = []


for artist, id in zip(df["artist_0"], df["artist_id"]):
    if pd.isnull(artist):
        continue
    track_lower = lower_case(artist)
    track_lower_no_punctuation = lower_case_remove_punctuation(artist)
    track_lower_no_the = remove_the(lower_case(artist))
    track_lower_no_punctuation_no_the = remove_the(
        lower_case_remove_punctuation(artist)
    )

    data.append((id, artist, track_lower))
    data.append((id, artist, track_lower_no_punctuation))
    data.append((id, artist, track_lower_no_the))
    data.append((id, artist, track_lower_no_punctuation_no_the))

conn_original.execute("""
    DROP TABLE IF EXISTS transformed_artists
""")
conn_original.execute("""
    CREATE TABLE IF NOT EXISTS transformed_artists (
        artist_id TEXT,
        original_artist TEXT,
        transformed_artist TEXT
    )
""")

conn_original.executemany(
    """
    INSERT INTO transformed_artists (artist_id, original_artist, transformed_artist)
    VALUES (?, ?, ?)
""",
    data,
)

conn_original.commit()
conn_original.close()

print("Nuovo database creato con i titoli delle canzoni trasformati!")
