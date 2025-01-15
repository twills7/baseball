import os

batting_categories = []
pitching_categories = []

def parse_batting_totals(year, batting_categories):
    year_data = []
    player_data = []
    data_folder = '/Users/tylerwilley/baseball/data/batting_totals'
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if os.path.isfile(file_path) and str(year) in filename:
            with open(file_path, 'r') as file:
                line_num = 0
                for line in file:
                    if line_num == 0:
                        line_num += 1
                        batting_categories.append(line.strip().split(','))
                        continue
                    else:
                        player_line = line.strip()
                        player_data = player_line.split(',')
                        year_data.append(player_data)
                        line_num += 1
    return year_data

def parse_pitching_totals(year, pitching_categories):
    year_data = []
    player_data = []
    data_folder = '/Users/tylerwilley/baseball/data/pitching_totals'
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if os.path.isfile(file_path) and str(year) in filename:
            with open(file_path, 'r') as file:
                line_num = 0
                for line in file:
                    if line_num == 0:
                        line_num += 1
                        pitching_categories.append(line.strip().split(','))
                        continue
                    else:
                        player_line = line.strip()
                        player_data = player_line.split(',')
                        year_data.append(player_data)
                        line_num += 1
    return year_data

year = input('Enter year: ')
batting_data = parse_batting_totals(year, batting_categories)
pitching_data = parse_pitching_totals(year, pitching_categories)

for player in batting_data:
    print(player)

for player in pitching_data:
    print(player)

print(batting_categories)
print(pitching_categories)