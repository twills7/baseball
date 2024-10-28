import statsapi as mlb

# Function to lookup player ID
def lookup_player_id(name):
    players = mlb.lookup_player(name)
    return players[0]['id']

# Function to lookup team ID
def lookup_team_id(name):
    teams = mlb.lookup_team(name)
    return teams[0]['id']

# Function to get hitting stats
def get_hitter_stats(player_id):
    player = mlb.player_stat_data(player_id, group='hitting')
    for key, value in player.items():
        print(key, value)
        if key == 'stats':
            print(calculate_player_value(value[0]['stats'], 'hitter'))
    return player

# Function to get pitching stats
def get_pitcher_stats(player_id):
    player = mlb.player_stat_data(player_id, group='pitching')
    for key, value in player.items():
        print(key, value)
        if key == 'stats':
            calculate_player_value(value[0]['stats'], 'hitter')
    return player

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
        value += float(stats['homeRuns']) * 10    # Home Runs weight
        value += float(stats['rbi']) * 3    # Runs Batted In weight
        value += float(stats['stolenBases']) * 4     # Stolen Bases weight
        value += float(stats['runs']) * 3   # Runs weight
        value -= float(stats['strikeOuts']) * 2 # Strikeouts weight
        value -= float(stats['caughtStealing']) * 2 # Caught Stealing weight
        value += float(stats['walks']) * 2 # Walks weight
        value += float(stats['hits']) * 2   # Hits weight
        value -= float(stats['groundIntoDoublePlay']) * 5 # Ground Into Double Play weight
        value += float(stats['doubles']) * 4 # Doubles weight
        value += float(stats['triples']) * 7    # Triples weight
        value += float(stats['hitByPitch']) * 2 # Hit By Pitch weight

    elif player_type == 'pitcher':
        # Pitchers: each stat is weighted based on its typical impact on value
        value += stats.get('W', 0) * 5      # Wins weight
        value += stats.get('K', 0) * 2      # Strikeouts weight
        value -= stats.get('ERA', 0) * 75   # Earned Run Average weight (lower is better)
        value -= stats.get('WHIP', 0) * 50  # Walks + Hits per Inning Pitched (lower is better)

    return value

for player in mlb.roster(input('Enter team name:')):
    get_hitter_stats(player[lookup_player_id(player['name'])])

