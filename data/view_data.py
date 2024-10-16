import sqlite3

# Connessione al tuo file .db
db_path = 'final_database.db'  # Sostituisci con il percorso del file .db
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Lista delle tabelle nel database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabelle nel database:")
for table in tables:
    print(table[0])

# Mostra la struttura di ogni tabella
for table in tables:
    print(f"\nStruttura della tabella {table[0]}:")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for column in columns:
        print(f"Colonna: {column[1]}, Tipo: {column[2]}")

# Chiudi la connessione al database
# Esegui una query per vedere una riga del database (puoi modificare la query per cercare una canzone specifica)
cursor.execute("SELECT * FROM music LIMIT 100")  # Cambia "extracted" con il nome della tua tabella

# Prendi tutte le 10 righe
rows = cursor.fetchall()

# Stampa tutte le righe
for row in rows:
    print(row)

# Chiudi la connessione al database
conn.close()