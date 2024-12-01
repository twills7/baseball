import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('player_stats.db')
cursor = conn.cursor()

# Query to select all data from the player_stats table
cursor.execute('SELECT * FROM player_stats')

# Fetch all rows from the result of the query
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()