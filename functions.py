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
    fielding = mlb.player_stat_data(player_id, group='fielding')
    name = player['first_name'] + ' ' + player['last_name']
    for key, value in player.items():
        if key == 'stats':
            mvs = calculate_player_value(value[0]['stats'], 'hitter')
            games = value[0]['stats']['gamesPlayed']
    for key, value in fielding.items():
        if key == 'stats':
            mvs += calculate_player_value(value[0]['stats'], 'fielder')
    return name, mvs, games

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
