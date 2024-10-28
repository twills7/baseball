import matplotlib.pyplot as plt
import functions as f

def plot_player_value(name):
    player_id = f.lookup_player_id(name)
    player = f.get_hitter_stats(player_id)
    plt.bar(player[0], player[1])
    plt.title('Player Value for ' + player[0])
    plt.xlabel('Player')
    plt.ylabel('Value')
    plt.show()

plot_player_value('Mike Trout')
