import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotVariance(variances, filenameOutput = "./variance.pdf", varEnv=None):
    rounds = ["Round 1", "Round 2", "Round 3", "Round 4"]

    # # Identify player columns dynamically
    # player_columns = [col for col in dataframe.columns if col.startswith('player_')]

    # # Calculate variance for each round
    # for index, row in dataframe.iterrows():
    #     player_scores = list(row[player_columns])
    #     variance = np.var(player_scores)
    #     variances.append(round(variance, 2))
    
    # Plotting the variances
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, variances, marker='o')
    plt.xlabel('Round')
    plt.ylabel('Variance')
    plt.xticks(["Round 1", "Round 2", "Round 3", "Round 4"])
    plt.grid(True)
    plt.savefig(filenameOutput, dpi = 300)
    if varEnv != None and varEnv["verbosity"] != 0: plt.show()

def plotVarianceAll(variances, filenameOutput = "./variance.pdf", varEnv=None):
    plt.rcParams.update({'font.size': 28})
    rounds = ["Round 1", "Round 2", "Round 3", "Round 4"]
    plt.figure(figsize=(12, 8))
    for label, variances in variances.items():
        plt.plot(rounds, variances, marker='o', label = label)
    plt.xlabel('Round')
    plt.ylabel('Variance')
    plt.xticks(["Round 1", "Round 2", "Round 3", "Round 4"])
    plt.legend()
    plt.grid(True)
    plt.savefig(filenameOutput, dpi = 300)
    if varEnv != None and varEnv["verbosity"] != 0: plt.show()