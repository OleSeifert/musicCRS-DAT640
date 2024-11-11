import sqlite3

# Connetti al database SQLite
conn = sqlite3.connect('final_database.db')  # sostituisci con il percorso del tuo file DB
cursor = conn.cursor()

# Conta il numero di righe prima della cancellazione
cursor.execute("SELECT COUNT(*) FROM music")  # sostituisci con il nome della tua tabella
total_rows_before = cursor.fetchone()[0]

# Esegui la cancellazione delle righe con acousticness null
cursor.execute("DELETE FROM music WHERE acousticness IS NULL")  # sostituisci con il nome della tua tabella
conn.commit()

cursor.execute("DELETE FROM music WHERE track_popularity IS NULL")  # sostituisci con il nome della tua tabella
conn.commit()
# Conta il numero di righe dopo la cancellazione
cursor.execute("SELECT COUNT(*) FROM music")
total_rows_after = cursor.fetchone()[0]

# Calcola quante righe sono state eliminate
deleted_rows = total_rows_before - total_rows_after

# Mostra il numero di righe eliminate
print(f"Numero di righe eliminate: {deleted_rows}")

# Chiudi la connessione al DB
conn.close()
