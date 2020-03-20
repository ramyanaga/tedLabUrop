import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from representations.sequentialembedding import SequentialEmbedding

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

'''
This function plots 3 lines per stim word --
one for (stim, high), (stim, low), (stim, incon);
each point of each line is the average of the similarity
scores for years at and before that point
'''

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

def plotLines(startDecade, endDecade):
    wordPairsList = parseTxtFile()
    figureCount = 0
    years = [i for i in range(startDecade, endDecade, 10)]
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(startDecade, endDecade, 10))
    yearHighVals, yearLowVals, yearLowVals = [], [], []
    for wordList in wordPairsList:
        if len(wordList) < 4:
            continue
        stimWord = wordList[0]
        highVals, lowVals, inconVals = [], [], []
        highCounter, lowCounter, inconCounter = 0, 0, 0
        high, low, incongruent = wordList[1], wordList[2], wordList[3]      
        time_sim_high = real_embeddings.get_time_sims(stimWord, high)
        time_sim_low = real_embeddings.get_time_sims(stimWord, low)
        time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

        for sim_year, sim in time_sim_high.iteritems():
            highVals.append(sim)
        
        for sim_year, sim in time_sim_low.iteritems():
            lowVals.append(sim)
        
        for sim_year, sim in time_sim_incon.iteritems():
            inconVals.append(sim)
    
        plt.figure()
        plt.plot(years, highVals, 'g')
        plt.plot(years, lowVals, 'r')
        plt.plot(years, inconVals, 'm')
        plotTitle = stimWord + " " + "(" + high + ", " + low + ", " + incongruent + ", " + ")"

        plotFileName = "individualLineGraphs/" + stimWord + "_" + high + "_" + low + "_" + incongruent
        plt.title(plotTitle)
        plt.savefig(plotFileName)
        plt.close()


def plotAveragedLines(startDecade, endDecade):
    wordPairsList = parseTxtFile()
    figureCount = 0
    years = [i for i in range(startDecade, endDecade, 10)]
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(startDecade, endDecade, 10))
    yearHighVals, yearLowVals, yearInconVals = [], [], []
    for wordList in wordPairsList:
        if len(wordList) < 4:
            continue
        stimWord = wordList[0]
        highAvgs, lowAvgs, inconAvgs = [], [], []
        highCounter, lowCounter, inconCounter = 0,0,0
        high, low, incongruent = wordList[1], wordList[2], wordList[3]
        time_sim_high = real_embeddings.get_time_sims(stimWord, high)
        time_sim_low = real_embeddings.get_time_sims(stimWord, low)
        time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

        for sim_year, sim in time_sim_high.iteritems():
            nextHigh = (sum(highAvgs) + sim)/(len(highAvgs) + 1)
            highAvgs.append(nextHigh)
        
        for sim_year, sim in time_sim_low.iteritems():
            nextLow = (sum(lowAvgs) + sim)/(len(lowAvgs) + 1)
            lowAvgs.append(nextLow)
        
        for sim_year, sim in time_sim_incon.iteritems():
            nextIncon = (sum(inconAvgs) + sim)/(len(inconAvgs) + 1)
            inconAvgs.append(nextIncon)

        plt.figure()
        plt.plot(years, highAvgs, 'g')
        plt.plot(years, lowAvgs, 'r')
        plt.plot(years, inconAvgs, 'm')
        plotTitle = stimWord + " " + "(" + high + ", " + low + ", " + incongruent + ", " + ")"
        plotFileName = "averagedLineGraphs/" + stimWord + "_" + high + "_" + low + "_" + incongruent
        plt.title(plotTitle)
        plt.savefig(plotFileName)
        plt.close()

#plotAveragedLines(startDecade=1800, endDecade=2000)
plotLines(startDecade=1800, endDecade=2000)