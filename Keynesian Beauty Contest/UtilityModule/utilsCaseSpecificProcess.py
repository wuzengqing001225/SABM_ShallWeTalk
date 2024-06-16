def caluWinner(listChoices):
    avgChoices = sum(listChoices) / len(listChoices)
    avgTwoThird = avgChoices * 2.0 / 3.0

    differences = [abs(x - avgTwoThird) for x in listChoices]
    minDifference = min(differences)
    indexWinner = [index + 1 for index, diff in enumerate(differences) if diff == minDifference]
    
    return avgChoices, avgTwoThird, indexWinner
