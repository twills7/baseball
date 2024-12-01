import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('player_stats.db')
cursor = conn.cursor()

# SQL command to create the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,                    -- Player name
        games_played INTEGER,                  -- Number of games played
        ground_outs INTEGER,                   -- Number of ground outs
        runs INTEGER,                          -- Number of runs
        doubles INTEGER,                       -- Number of doubles
        triples INTEGER,                       -- Number of triples
        home_runs INTEGER,                     -- Number of home runs
        strike_outs INTEGER,                   -- Number of strike outs
        base_on_balls INTEGER,                 -- Number of base on balls
        intentional_walks INTEGER,            -- Number of intentional walks
        hits INTEGER,                          -- Number of hits
        hit_by_pitch INTEGER,                  -- Number of times hit by pitch
        avg REAL,                              -- Batting average
        at_bats INTEGER,                       -- Number of at bats
        obp REAL,                              -- On base percentage
        slg REAL,                              -- Slugging percentage
        ops REAL,                              -- On base plus slugging
        caught_stealing INTEGER,              -- Number of times caught stealing
        stolen_bases INTEGER,                 -- Number of stolen bases
        ground_into_double_play INTEGER,      -- Number of ground into double play
        number_of_pitches INTEGER,            -- Number of pitches
        plate_appearances INTEGER,            -- Number of plate appearances
        total_bases INTEGER,                  -- Total bases
        rbi INTEGER,                          -- Runs batted in
        left_on_base INTEGER,                 -- Number of left on base
        sac_bunts INTEGER,                    -- Number of sacrifice bunts
        sac_flies INTEGER,                    -- Number of sacrifice flies
        babip REAL,                            -- Batting average on balls in play
        ground_outs_to_airouts REAL          -- Ground outs to air outs ratio
    )
''')

# Commit the changes (create the table)
conn.commit()

# Commit the changes (insert the data)
conn.commit()

print("Table created and data inserted successfully!")

# Close the cursor and connection
cursor.close()
conn.close()