import statsapi as mlb
import sqlite3

# Function to lookup player ID
def lookup_player_id(name):
    players = mlb.lookup_player(name)
    if len(players) == 0:
        return 0
    return players[0]['id']

# Function to lookup team ID
def lookup_team_id(name):
    teams = mlb.lookup_team(name)
    return teams[0]['id']

# Function to get hitting stats
def get_hitter_stats(player_id):
    player = mlb.player_stat_data(player_id, group='hitting')
    fielding = mlb.player_stat_data(player_id, group='fielding')
    name = player['first_name'] + ' ' + player['last_name']
    # for key, value in player.items():
    #     if key == 'stats':
    #         mvs = calculate_player_value(value[0]['stats'], 'hitter')
    #         games = value[0]['stats']['gamesPlayed']
    # for key, value in fielding.items():
    #     if key == 'stats':
    #         mvs += calculate_player_value(value[0]['stats'], 'fielder')
    return name

# Function to get pitching stats
def get_pitcher_stats(player_id):
    player = mlb.player_stat_data(player_id, group='pitching')
    for key, value in player.items():
        if key == 'stats':
            mvs = calculate_player_value(value[0]['stats'], 'fielding')
    return mvs

# Function to get team stats
def get_team_stats(team_id):
    team = mlb.team_stats(team_id)
    return team

# Function to get team roster
def get_team_roster(team_id):
    roster = mlb.roster(team_id)
    return roster

def calculate_player_value(stats, player_type):
    """
    Calculate a value for an MLB player based on their stats.

    Parameters:
    - stats (dict): A dictionary containing player stats.
    - player_type (str): Type of player ('hitter' or 'pitcher').

    For hitters, expected stats keys are: 'BA', 'OBP', 'SLG', 'HR', 'RBI', 'SB'.
    For pitchers, expected stats keys are: 'ERA', 'WHIP', 'K', 'W'.

    Returns:
    - float: Calculated player value.
    """
    value = 0
    if player_type == 'hitter':
        # Hitters: each stat is weighted based on its typical impact on value
        value += float(stats['homeRuns']) * 9    # Home Runs weight
        value += float(stats['stolenBases']) * 1.25     # Stolen Bases weight
        value -= float(stats['strikeOuts']) * 1 # Strikeouts weight
        value -= float(stats['groundOuts']) * 0.97 # Groundouts weight
        value -= float(stats['airOuts']) * 0.9 # Groundouts weight
        value -= float(stats['caughtStealing']) * 2 # Caught Stealing weight
        value += float(stats['baseOnBalls']) * 2 # Walks weight
        value += (float(stats['hits']) - float(stats['doubles']) - float(stats['homeRuns']) - float(stats['triples'])) * 3   # Hits weight
        value -= float(stats['groundIntoDoublePlay']) * 2 # Ground Into Double Play weight
        value += float(stats['doubles']) * 4.5 # Doubles weight
        value += float(stats['triples']) * 6.6   # Triples weight
        value += float(stats['hitByPitch']) * 2 # Hit By Pitch weight

    elif player_type == 'fielder':
        # Fielders: each stat is weighted based on its typical impact on value
        value += float(stats['assists']) * 0.5
        value += float(stats['putOuts']) * 0.1
        value += float(stats['errors']) * -1.2


    elif player_type == 'pitcher':
        # Pitchers: each stat is weighted based on its typical impact on value
        value += float(stats['strikeOuts']) * 2.5   # Strikeouts weight
        value += float(stats['wins']) * 6   # Wins weight
        value -= float(stats['losses']) * 4    # Losses weight
        value -= float(stats['hits']) * 0.6     # Hits weight
        value -= float(stats['homeRuns']) * 1.5     # Home Runs weight
        value -= float(stats['baseOnBalls']) * 1.5      # Walks weight
        value -= float(stats['earnedRuns']) * 2.5   # Earned Runs weight
        value += float(stats['inningsPitched']) * 2.25  # Innings Pitched weight


    return value

def value_finder():
    name = input('Enter player name: ')
    while name != 'exit':
        fullname, mvs, games = get_hitter_stats(lookup_player_id(name))
        print(f'{fullname}\'s value is {mvs:.2f}')
        print(f'Per game value: {mvs/games:.2f}')
        name = input('Enter player name: ')

def fill_database(player_id):
    conn = sqlite3.connect('player_stats.db')
    cursor = conn.cursor()
    name = get_hitter_stats(player_id)
    stats = mlb.player_stat_data(lookup_player_id(name), group='hitting')
    for key, value in stats.items():
        if key == 'stats':
            games_played = value[0]['stats']['gamesPlayed']
            ground_outs = value[0]['stats']['groundOuts']
            runs = value[0]['stats']['runs']
            doubles = value[0]['stats']['doubles']
            triples = value[0]['stats']['triples']
            home_runs = value[0]['stats']['homeRuns']
            strike_outs = value[0]['stats']['strikeOuts']
            base_on_balls = value[0]['stats']['baseOnBalls']
            intentional_walks = value[0]['stats']['intentionalWalks']
            hits = value[0]['stats']['hits']
            hit_by_pitch = value[0]['stats']['hitByPitch']
            avg = value[0]['stats']['avg']
            at_bats = value[0]['stats']['atBats']
            obp = value[0]['stats']['obp']
            slg = value[0]['stats']['slg']
            ops = value[0]['stats']['ops']
            caught_stealing = value[0]['stats']['caughtStealing']
            stolen_bases = value[0]['stats']['stolenBases']
            ground_into_double_play = value[0]['stats']['groundIntoDoublePlay']
            number_of_pitches = value[0]['stats']['numberOfPitches']
            plate_appearances = value[0]['stats']['plateAppearances']
            total_bases = value[0]['stats']['totalBases']
            rbi = value[0]['stats']['rbi']
            left_on_base = value[0]['stats']['leftOnBase']
            sac_bunts = value[0]['stats']['sacBunts']
            sac_flies = value[0]['stats']['sacFlies']
            babip = value[0]['stats']['babip']
            ground_outs_to_airouts = value[0]['stats']['groundOutsToAirouts']
    cursor.execute('''
        INSERT INTO player_stats (name, games_played, ground_outs, runs, doubles, triples, home_runs, strike_outs, base_on_balls, intentional_walks, hits, hit_by_pitch, avg, at_bats, obp, slg, ops, caught_stealing, stolen_bases, ground_into_double_play, number_of_pitches, plate_appearances, total_bases, rbi, left_on_base, sac_bunts, sac_flies, babip, ground_outs_to_airouts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, games_played, ground_outs, runs, doubles, triples, home_runs, strike_outs, base_on_balls, intentional_walks, hits, hit_by_pitch, avg, at_bats, obp, slg, ops, caught_stealing, stolen_bases, ground_into_double_play, number_of_pitches, plate_appearances, total_bases, rbi, left_on_base, sac_bunts, sac_flies, babip, ground_outs_to_airouts))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'{name} added to database.')

def fill_league_stats():
    print('Getting each team values...', end = "", flush=True)
    for i in range(108, 122): # 108-121 are the team IDs for MLB teams
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=12)
        print('.', end = "", flush=True)
        for player in roster:
            player_id = lookup_player_id(player[1])
            if player_id != 0:
                fill_database(player_id)
    for i in range(133, 148): # 108-121 are the team IDs for MLB teams
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=12)
        print('.', end = "", flush=True)
        for player in roster:
            player_id = lookup_player_id(player[1])
            if player_id != 0:
                fill_database(player_id)
    roster = mlb.team_leader_data(158, "atBats", "2024", limit=12)
    print('.', end = "", flush=True)
    for player in roster:
        player_id = lookup_player_id(player[1])
        if player_id != 0:
            fill_database(player_id)


if __name__ == '__main__':
    choice = input('Enter 1 to find player value, 2 to fill database, 3 to compare team stats, or 4 to completely fill database: ')
    while choice > '0' and choice < '5':
        if choice == '1':
            value_finder()
        elif choice == '2':
            fill_database(lookup_player_id(input('Enter player name: ')))
        elif choice == '3':
            team_id = lookup_team_id(input('Enter team name: '))
            team = get_team_stats(team_id)
            print(f'{team["name"]}\'s stats:')
            for key, value in team.items():
                print(f'{key}: {value}')
        elif choice == '4':
            fill_league_stats()
        else:
            print('Invalid choice.')
        choice = input('Enter 1 to find player value, 2 to fill database, or 3 to compare team stats: ')