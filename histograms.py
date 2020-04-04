import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from representations.sequentialembedding import SequentialEmbedding

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

def parseTxtFile():
    """
    This function dumps all (stim word, high, low, inconcgruent) into
    one list per stim word
    """
    wordPairsList = []
    with open("wordPairs.txt", "r") as f:
        currentStimWordList = []
        for line in f:
            if " " in line:
                wordPairsList.append(currentStimWordList)
                currentStimWordList = []
                splitLine = line.split(" ")
                stimWord = splitLine[-1][:-2]
                currentStimWordList.append(stimWord)
            else:
                currentStimWordList.append(line[:-2])

    return wordPairsList[1:]


def pltHistograms():
    wordList = parseTxtFile()
    yearHigh, yearLow, yearIncon = {}, {}, {}
    startDecade, endDecade = 1800, 2000
    years = [year for year in range(startDecade, endDecade, 10)]
    for year in years:
        yearHigh[year] = []
        yearLow[year] = []
        yearIncon[year] = []
    
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(startDecade, endDecade, 10))
    wordPairsList = parseTxtFile()
    for wordList in wordPairsList:
        if len(wordList) < 4:
            continue
        
        stimWord = wordList[0]
        high, low, incongruent = wordList[1], wordList[2], wordList[3]
        time_sim_high = real_embeddings.get_time_sims(stimWord, high)
        time_sim_low = real_embeddings.get_time_sims(stimWord, low)
        time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)
        for sim_year, sim in time_sim_high.iteritems():
            yearHigh[sim_year].append(sim)
        
        for sim_year, sim in time_sim_low.iteritems():
            yearLow[sim_year].append(sim)
        
        for sim_year, sim in time_sim_incon.iteritems():
            yearIncon[sim_year].append(sim)

    figCount = 0
    for year in yearHigh:
        plt.figure(figCount)
        plt.title("cosine sim histogram in year " + str(year))
        plt.xlabel("cosine sim scores")
        plt.ylabel("frequency of score")
        plt.hist(yearHigh[year], color='r')
        plt.hist(yearLow[year], color='b')
        plt.hist(yearIncon[year], color='g')
        plt.savefig("histograms/" + str(year))
        figCount += 1

pltHistograms()
                

