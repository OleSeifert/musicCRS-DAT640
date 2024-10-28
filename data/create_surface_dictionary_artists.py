import sqlite3
import pandas as pd
import re

# Funzioni di pulizia del testo
def lower_case(string):
    return string.lower()


def remove_punctuation(string):
    return string.replace("'", "").replace(",", "").replace(".", "").replace('"', "")


def lower_case_remove_punctuation(string):
    return lower_case(remove_punctuation(string))

#delete everithing inside parenthesises
def remove_parentheses(title):
    # Check if the title is fully enclosed in a single pair of parentheses
    if title.startswith("(") and title.endswith(")"):
        return title[1:-1]  # Remove only the surrounding parentheses

    # Otherwise, remove all content within any parentheses
    return re.sub(r'\(.*?\)', '', title).strip()

def remove_after_separator(title):
    if ' - ' in title:
        return title.split(' - ')[0]  # Restituisce solo la parte prima del separatore
    return title  # Restituisce il titolo originale se il separatore non è presente

#remove 'the' if is at the start of the string
def remove_the(title):
    if title.lower().startswith('the '):
        return title[4:]  # Restituisce il titolo senza 'the' iniziale
    return title



# Connessione al database SQLite originale
conn_original = sqlite3.connect('final_database.db')  # Sostituisci con il nome del tuo file .db
query = "SELECT artist_0 FROM music"  # Sostituisci con il nome della tua tabella

# Carica i dati in un DataFrame pandas
df = pd.read_sql_query(query, conn_original)
# Prepara i dati per il nuovo database
data = []

# Itera su ciascun titolo di brano
for artist in df['artist_0']:
    if pd.isnull(artist):
        continue
    # Applica ciascuna funzione all'intero titolo della canzone
    track_lower = lower_case(artist)
    track_lower_no_punctuation = lower_case_remove_punctuation(artist)
    track_lower_no_the = remove_the(lower_case(artist))
    track_lower_no_punctuation_no_the = remove_the(lower_case_remove_punctuation(artist))

    # Aggiungi le prime due righe (lowercase e senza punteggiatura)
    data.append((artist, track_lower))
    data.append((artist, track_lower_no_punctuation))
    data.append((artist, track_lower_no_the))
    data.append((artist, track_lower_no_punctuation_no_the))


# Crea la tabella nel nuovo database con solo 2 colonne
conn_original.execute('''
    CREATE TABLE IF NOT EXISTS transformed_artists (
        original_artist TEXT,
        transformed_artist TEXT
    )
''')

# Inserisci i dati nella nuova tabella
conn_original.executemany('''
    INSERT INTO transformed_artists (original_artist, transformed_artist)
    VALUES (?, ?)
''', data)

conn_original.commit()  # Salva le modifiche
conn_original.close()  # Chiudi la connessione al nuovo database

print("Nuovo database creato con i titoli delle canzoni trasformati!")

