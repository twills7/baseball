import matplotlib.pyplot as plt
import functions as f
import statsapi as mlb

def plot_player_value_comparison():
    name = input('Enter player name: ')
    while name:
        player1 = f.get_hitter_stats(f.lookup_player_id(name))
        print(f'{player1[0]}\'s value is {player1[1]:.2f}')
        plt.bar(player1[0], player1[1])
        name = input('Enter player name: ')
    plt.title('Player Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()

def plot_team_values():
    team_id = f.lookup_team_id(input('Enter team: '))
    roster = mlb.team_leader_data(team_id, "atBats", "2024", limit=100)
    values = []
    players = []
    print(roster)
    for player in roster:
        stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
        values.append(stats[1])
        players.append(stats[0])
        plt.bar(players, values)
    plt.title('Team Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()

def plot_league_stats():
    for i in range(108, 122): # 108-121 are the team IDs for MLB teams
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
        values = []
        players = []
        for player in roster:
            stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
            values.append(stats[1])
            players.append(stats[0])
            plt.bar(players, values)
    for i in range(133, 148): # 108-121 are the team IDs for MLB teams
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
        values = []
        players = []
        for player in roster:
            stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
            values.append(stats[1])
            players.append(stats[0])
            plt.bar(players, values)
    roster = mlb.team_leader_data(158, "atBats", "2024", limit=8)
    values = []
    players = []
    for player in roster:
        stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
        values.append(stats[1])
        players.append(stats[0])
        plt.bar(players, values)
    plt.title('Team Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()


def plot_team_total_stats():
    values = []
    teams = []
    for i in range(108, 122): # 108-121 are the team IDs for MLB teams
        total = 0
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
        for player in roster:
            stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
            total += stats[1]
        teams.append(mlb.lookup_team(i))
        values.append(total)
    '''for i in range(133, 148): # 108-121 are the team IDs for MLB teams
        total = 0
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
        for player in roster:
            stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
            total += stats[1]
        teams.append(mlb.lookup_team(i)[1])
        values.append(total)
    total = 0
    roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
    for player in roster:
        stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
        total += stats[1]
    teams.append(mlb.lookup_team(i)['name'])
    values.append(total)'''
    plt.bar(teams, values)
    plt.title('Team Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()
plot_team_total_stats()

