import datetime
import statsapi as mlb
import sqlite3

# Get roster for a team and return a list of player names
def get_roster(name):
    # Get team ID
    team_stats = mlb.lookup_team(name)
    print(team_stats)
    id = team_stats[0]['id']

    # Get roster for team
    roster_names = mlb.roster(id, rosterType=None, season=2024, date=None)
    roster =  roster_names.splitlines()

    names = []
    for i in range(len(roster)):
        roster[i] = roster[i].split(' ')
        names.append([roster[i][-2] + ' ' + roster[i][-1]])

    return names

# Get each player's player id
def get_player_id(name, year):
    player = mlb.lookup_player(name, season=year)
    if player:
        return player[0]['id']
    else:
        player = mlb.lookup_player(name.split(' ')[1])
        if player:
            return player[0]['id']
        else:
            return 0
        
# Get hitting stats
def get_hitting_stats(player_id):
    player = mlb.player_stat_data(player_id, group='hitting')
    if player['stats']:
        return player['stats'][0]['stats']
    else:
        player = mlb.player_stat_data(player_id, group='pitching')
        if player['stats'][0]:
            return player['stats'][0]['stats']
        else:
            return 0
        
# Get pitching stats
def get_pitching_stats(player_id):
    player = mlb.player_stat_data(player_id, group='pitching')
    if player['stats']:
        return player['stats'][0]['stats']
    else:
        return 0

# Get fielding stats
def get_fielding_stats(player_id):
    player = mlb.player_stat_data(player_id, group='fielding')
    if player['stats']:
        return player['stats'][0]['stats']
    else:
        return 0
    
def populate_database(roster):
    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('player_stats.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stats (
        name TEXT NOT NULL,                    -- Player name
        player_id INTEGER PRIMARY KEY,         -- Player ID
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
    conn.commit()
    for i in roster:
        stats = i[2]
        if stats != 0 and len(stats) < 33:
            games_played = stats['gamesPlayed']
            ground_outs = stats['groundOuts']
            runs = stats['runs']
            doubles = stats['doubles']
            triples = stats['triples']
            home_runs = stats['homeRuns']
            strike_outs = stats['strikeOuts']
            base_on_balls = stats['baseOnBalls']
            intentional_walks = stats['intentionalWalks']
            hits = stats['hits']
            hit_by_pitch = stats['hitByPitch']
            avg = stats['avg']
            at_bats = stats['atBats']
            obp = stats['obp']
            slg = stats['slg']
            ops = stats['ops']
            caught_stealing = stats['caughtStealing']
            stolen_bases = stats['stolenBases']
            ground_into_double_play = stats['groundIntoDoublePlay']
            number_of_pitches = stats['numberOfPitches']
            plate_appearances = stats['plateAppearances']
            total_bases = stats['totalBases']
            rbi = stats['rbi']
            left_on_base = stats['leftOnBase']
            sac_bunts = stats['sacBunts']
            sac_flies = stats['sacFlies']
            babip = stats['babip']
            ground_outs_to_airouts = stats['groundOutsToAirouts']
            cursor.execute('''
                INSERT INTO player_stats (name, games_played, ground_outs, runs, doubles, triples, home_runs, strike_outs, base_on_balls, intentional_walks, hits, hit_by_pitch, avg, at_bats, obp, slg, ops, caught_stealing, stolen_bases, ground_into_double_play, number_of_pitches, plate_appearances, total_bases, rbi, left_on_base, sac_bunts, sac_flies, babip, ground_outs_to_airouts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (i[0], games_played, ground_outs, runs, doubles, triples, home_runs, strike_outs, base_on_balls, intentional_walks, hits, hit_by_pitch, avg, at_bats, obp, slg, ops, caught_stealing, stolen_bases, ground_into_double_play, number_of_pitches, plate_appearances, total_bases, rbi, left_on_base, sac_bunts, sac_flies, babip, ground_outs_to_airouts))
            
            conn.commit()
            print(f'{i[0]} added to database.')

    cursor.close()
    conn.close()






print("Database populated successfully.")

id = get_player_id('Ty Adcock', 2024)
print(get_hitting_stats(id))
id = get_player_id('Pete Alonso', 2024)
print(get_hitting_stats(id))

roster = get_roster(input("Enter a team name: "))
for i in range(len(roster)):
    roster[i].append(get_player_id(roster[i][0], 2024))
    roster[i].append(get_hitting_stats(roster[i][1]))
    roster[i].append(get_pitching_stats(roster[i][1]))
    roster[i].append(get_fielding_stats(roster[i][1]))
    print(roster[i][0])
    print(len(roster[i][2]))

populate_database(roster)
print(roster)