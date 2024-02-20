import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_hist_for_choices(record_date, record_time, task):

    file_path = f'./output/record_{record_date}_{record_time}_task{task}/{record_date}_{record_time}_overview.csv'

    df = pd.read_csv(file_path)

    score_columns = [col for col in df.columns if col not in ['Round', 'Winning Guess', 'Round Average', 'Winner']]
    scores = df[score_columns]

    scores = scores.apply(pd.to_numeric, errors='coerce')
    min_score = scores.min().min()
    max_score = scores.max().max()
    print(scores, min_score, max_score)

    flattened_scores = scores.values.flatten()
    flattened_scores = flattened_scores[~np.isnan(flattened_scores)]

    plt.hist(flattened_scores, bins=range(int(min_score), int(max_score)+1))
    plt.title('Histogram of Player Scores')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.xlim(min_score, max_score)
    plt.show()
    plt.savefig(f"figure/{record_date}_{record_time}_{task}.png")
    plt.close()


def plot_hist_for_choices_one_round(record_date, record_time, task):

    file_path = f'./output/record_{record_date}_{record_time}_task{task}/{record_date}_{record_time}_overview.csv'

    df = pd.read_csv(file_path)
    df = df[df['Round'] == 1]

    score_columns = [col for col in df.columns if col not in ['Round', 'Winning Guess', 'Round Average', 'Winner']]
    scores = df[score_columns]

    scores = scores.apply(pd.to_numeric, errors='coerce')
    min_score = scores.min().min()
    max_score = scores.max().max()
    print(scores, min_score, max_score)

    flattened_scores = scores.values.flatten()
    flattened_scores = flattened_scores[~np.isnan(flattened_scores)]

    plt.hist(flattened_scores, bins=range(int(min_score), int(max_score)+1))
    plt.title('Histogram of Player Scores')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.xlim(min_score, max_score)
    plt.show()
    plt.savefig(f"figure/{record_date}_{record_time}_{task}.png")
    plt.close()


def plot_one_player_choices(record_date, record_time, task, player_id):
    file_path = f'./output/record_{record_date}_{record_time}_task{task}/{record_date}_{record_time}_player.csv'

    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    df = df[df['Player ID'] == player_id]
    x = df["Round"]
    y = df["Choice"]
    plt.plot(x, y)
    plt.title(f"Choices of Player {player_id}")
    plt.xlabel("Round")
    plt.ylabel("Choice")
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.yticks(range(0, 101, 5))
    plt.show()
    plt.savefig(f"figure/{record_date}_{record_time}_{task}_player{player_id}.png")
    plt.close()



if __name__ == '__main__':
    # record_date = '240107'
    # record_time = '0212'
    # task = 'Default'
    record_date = '240127'
    record_time = '2352'
    task = '3-5(reverse_nothing)'

    plot_hist_for_choices_one_round(record_date, record_time, task)
    # for i in range(1, 11):
    #     plot_one_player_choices(record_date, record_time, task, i)
