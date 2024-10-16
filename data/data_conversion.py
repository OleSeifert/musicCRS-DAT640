import sqlite3
import pandas as pd

df = pd.read_csv('spotify_data_12_20_2023.csv')

conn = sqlite3.connect('final_database.db')

# Converting the DataFrame to a SQL table
df.to_sql('music', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully!")