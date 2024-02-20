import matplotlib.pyplot as plt
import os
import fnmatch
import pandas as pd
import numpy as np
from matplotlib.ticker import PercentFormatter

LEGEND_FONT = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 14,
         }

LABEL_FONT = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 18,
         }

TITLE_FONT = {'family': 'Times New Roman',
         'weight': 'black',
         'size': 18,
         }

def read_choices(exp_name):
    root_dir = f"exp_data/{exp_name}"
    data = []
    for root, dirs, files in os.walk(root_dir):
        for dir in dirs:
            for sub_root, subdirs, sub_files in os.walk(os.path.join(root, dir)):
                for sub_file in fnmatch.filter(sub_files, '*overview.csv'):
                    file_path = os.path.join(sub_root, sub_file)
                    df = pd.read_csv(file_path)
                    record = df.iloc[0, 1:-2].tolist()
                    data.append(record)
    data = np.array(data).T
    # print(data.shape)
    return data

def boxplot(ax, exp_name, title):
    data = read_choices(exp_name)
    # plt.figure(figsize=(14, 7))
    # print(data)
    bp = ax.boxplot(data[1:, :], patch_artist=True, showmeans=False, showfliers=False)
    # print(data[1:])

    for box in bp['boxes']:
        box.set(color='blue', linewidth=2)
        box.set(facecolor='lightblue')

    # plt.setp(bp['fliers'], markeredgecolor='red', marker='o')
    # plt.setp(bp['medians'], color='red')
    # plt.setp(bp['means'], marker='D', markeredgecolor='green')
    if exp_name == "independent":
        print(data[:, :])
        print(data[:1,:])
    for i, wn in enumerate(data[:1,:].T):
        ax.plot(i + 1, wn, 'ro')

    # ax.set_title(title, TITLE_FONT)
    ax.set_xlabel('Run', LABEL_FONT)
    ax.set_ylabel('Number Choice', LABEL_FONT)
    ax.set_xticks(range(1, data.shape[1] + 1), [f'Run {i + 1}' for i in range(data.shape[1])])
    # plt.grid(True)
    # plt.show()
    # plt.savefig(f'figure/{title}.png')
    # plt.close()

def boxplot_one_figure(exp_name, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    boxplot(ax, exp_name, title)
    plt.tight_layout()
    plt.savefig(f'figure/boxplot_{exp_name}.png')
    plt.close()

def boxplot_rewarding_rules():
    fig, axs = plt.subplots(3, 1, figsize=(18, 18))
    boxplot(axs[0], "default", "Amplified reward")
    boxplot(axs[1],"independent", "Independent reward")
    boxplot(axs[2],"nothing", "Exclusive reward")
    plt.tight_layout()
    plt.savefig(f'figure/boxplot_rewarding_rules.png')
    plt.close()

def boxplot_personas():
    fig, axs = plt.subplots(4, 1, figsize=(18, 24))
    boxplot(axs[0], "default", "No persona")
    boxplot(axs[1],"all_agreeable", "All agreeable")
    boxplot(axs[2],"all_disagreeable", "All disagreeable")
    boxplot(axs[3], "mixed", "Mixed personas")
    plt.tight_layout()
    plt.savefig(f'figure/boxplot_personas.png')
    plt.close()

def boxplot_comm():
    fig, axs = plt.subplots(2, 1, figsize=(18, 24))
    boxplot(axs[0], "default", "With conversation")
    boxplot(axs[1],"no_comm", "No conversation")
    plt.tight_layout()
    plt.savefig(f'figure/boxplot_comm.png')
    plt.close()

def calc_cv(exp_name):
    data = read_choices(exp_name)[1:]
    # print(data)
    means = np.mean(data, axis=0)
    # print(means)
    std_devs = np.std(data, axis=0)
    # print(std_devs)
    cvs = std_devs / means
    cvs = np.nan_to_num(cvs)

    return cvs.mean()


def barplot_personas():
    # Sample data
    categories = ['No persona', 'All agreeable', 'All disagreeable', 'Mixed persona']
    collab_rates = [70, 100, 20, 100]
    cvs = []
    for exp_name in ["default", "all_agreeable", "all_disagreeable", "mixed"]:
        cv = calc_cv(exp_name) * 100
        cvs.append(cv)

    index = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))
    bars1 = ax.bar(index, collab_rates, width, label='Collab. rate')
    bars2 = ax.bar(index + width, cvs, width, label='%RSD')

    ax.set_ylabel('Percentage', LABEL_FONT)
    # ax.set_title('Comparison of persona distributions', TITLE_FONT)
    ax.set_xticks(index + width / 2)
    ax.set_xticklabels(categories)
    ax.legend(prop=LEGEND_FONT)
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    # plt.xticks(rotation=45)  # Rotate category names for better visibility

    plt.tight_layout()
    plt.savefig(f'figure/barplot_personas.png')
    plt.close()


if __name__ == '__main__':
    # read_choices("default")
    # boxplot_rewarding_rules()
    # plot_personas()
    # plot_comm()
    # barplot_personas()
    # print(calc_cv("default"))
    # print(calc_cv("independent"))
    # print(calc_cv("nothing"))
    boxplot_one_figure("default", "With conversation")
    boxplot_one_figure("no_comm", "No conversation")
    boxplot_one_figure("gpt3.5_comm", "With conversation")
    boxplot_one_figure("gpt3.5_no_comm", "No conversation")