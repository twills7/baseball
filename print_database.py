import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('player_stats.db')
cursor = conn.cursor()

# Query to select all data from the player_stats table
cursor.execute('SELECT * FROM player_stats')

# Fetch all rows from the result of the query
rows = cursor.fetchall()

# Remove duplicate names from the player_stats table
unique_rows = {}
for row in rows:
    name = row[0]  # Assuming the name is the first column
    if name not in unique_rows:
        unique_rows[name] = row
    else:
        cursor.execute('DELETE FROM player_stats WHERE name = ? AND rowid != ?', (name, row[0]))
# Update rows to only contain unique entries
rows = list(unique_rows.values())


# Commit the changes to the database
conn.commit()

# Print each row
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()