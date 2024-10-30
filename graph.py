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
    print('Getting player values...', end = "", flush=True)
    roster = mlb.team_leader_data(team_id, "atBats", "2024", limit=100)
    values = []
    players = []
    for player in roster:
        print('.', end = "", flush=True)
        stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
        values.append(stats[1])
        players.append(stats[0])
        plt.bar(players, values)
    print()
    plt.title('Team Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()

def plot_league_stats():
    print('Getting each team values...', end = "", flush=True)
    for i in range(108, 122): # 108-121 are the team IDs for MLB teams
        roster = mlb.team_leader_data(i, "atBats", "2024", limit=8)
        print('.', end = "", flush=True)
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
        print('.', end = "", flush=True)
        for player in roster:
            stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
            values.append(stats[1])
            players.append(stats[0])
            plt.bar(players, values)
    roster = mlb.team_leader_data(158, "atBats", "2024", limit=8)
    values = []
    players = []
    print('.', end = "", flush=True)
    for player in roster:
        stats = f.get_hitter_stats(f.lookup_player_id(player[1]))
        values.append(stats[1])
        players.append(stats[0])
        plt.bar(players, values)
    plt.title('Team Value Comparison')
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()

if __name__ == '__main__':
    choice = input('Enter 1 to compare player values, 2 to compare team values, or 3 to compare league stats: ')
    while choice > '0' and choice < '4':
        if choice == '1':
            plot_player_value_comparison()
        elif choice == '2':
            plot_team_values()
        elif choice == '3':
            plot_league_stats()
        else:
            print('Invalid choice')
        choice = input('Enter 1 to compare player values, 2 to compare team values, or 3 to compare league stats: ')