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
            for k, v in value[0]['stats'].items():  
                print(k, v)
    return player

# Function to get pitching stats
def get_hitter_stats(player_id):
    player = mlb.player_stat_data(player_id, group='pitching')
    for key, value in player.items():
        print(key, value)
        if key == 'stats':
            for k, v in value[0]['stats'].items():  
                print(k, v)
    return player

# Function to get team stats
def get_team_stats(team_id):
    team = mlb.team_stats(team_id)
    return team

# Function to get team roster
def get_team_roster(team_id):
    roster = mlb.roster(team_id)
    return roster

print(get_team_roster(lookup_team_id(input('Enter team name: '))))
