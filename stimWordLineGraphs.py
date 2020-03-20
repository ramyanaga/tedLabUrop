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

'''
stimWord = w_1, (high, low, incongruent) = w_j words
'''
def getContextSimScoreDenom(startDecade, endDecade, wordPairsList, real_embeddings):
    nonStimWords = []
    stimWordDenomMap = {} # map the triplet (stim, high, low, incon) to denom score b/c some stim words repeat
    for wordList in wordPairsList:
        if len(wordList) < 4:
            continue
        stimWord = wordList[0]
        high, low, incongruent = wordList[1], wordList[2], wordList[3]
        triplet = (stimWord, high, low, incongruent)     
        stimWordDenomMap[triplet] = {}
        
        time_sim_high = real_embeddings.get_time_sims(stimWord, high)
        time_sim_low = real_embeddings.get_time_sims(stimWord, low)
        time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

        for year in range(startDecade, endDecade, 10):
            yearSum = time_sim_high[year] + time_sim_low[year] + time_sim_high[year]
            stimWordDenomMap[triplet][year] = yearSum
    
    return stimWordDenomMap

        
def plotIndividualLines(startDecade, endDecade, averaged=False, contextRelevant=False):
    cosDenom = 0
    wordPairsList = parseTxtFile()
    figureCount = 0
    years = [i for i in range(startDecade, endDecade, 10)]
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(startDecade, endDecade, 10))
    yearHighVals, yearLowVals, yearLowVals = [], [], []
    stimWordDenomMap = {}
    if contextRelevant == True:
        stimWordDenomMap = getContextSimScoreDenom(startDecade, endDecade, wordPairsList, real_embeddings)
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
        triplet = (stimWord, high, low, incongruent) # only used if contextScores = true

        for sim_year, sim in time_sim_high.iteritems():
            if averaged:
                nextHigh = (sum(highVals) + sim)/(len(highVals) + 1)
                highVals.append(nextHigh)
            elif contextRelevant:
                nextHigh = sim/stimWordDenomMap[triplet][sim_year]
                highVals.append(nextHigh)
            else:
                highVals.append(sim)
        
        for sim_year, sim in time_sim_low.iteritems():
            if averaged:
                nextLow = (sum(lowVals) + sim)/(len(lowVals) + 1)
                lowVals.append(nextLow)
            elif contextRelevant:
                nextLow = sim/stimWordDenomMap[triplet][sim_year]
                lowVals.append(nextLow)
            else:
                lowVals.append(sim)
        
        for sim_year, sim in time_sim_incon.iteritems():
            if averaged:
                nextIncon = (sum(inconVals) + sim)/(len(inconVals) + 1)
                inconVals.append(nextIncon)
            elif contextRelevant:
                nextIncon = sim/stimWordDenomMap[triplet][sim_year]
                inconVals.append(nextIncon)
            else:
                inconVals.append(sim)
        
        plt.figure()
        plt.plot(years, highVals, 'g')
        plt.plot(years, lowVals, 'r')
        plt.plot(years, inconVals, 'm')
        plotTitle = stimWord + " " + "(" + high + ", " + low + ", " + incongruent + ", " + ")"

        if averaged:
            plotFileName = "averagedLineGraphs/" + stimWord + "_" + high + "_" + low + "_" + incongruent
        elif contextRelevant:
            plotFileName = "contextRelevantLineGraphs/" + stimWord + "_" + high + "_" + low + "_" + incongruent
        else:
            plotFileName = "individualLineGraphs/" + stimWord + "_" + high + "_" + low + "_" + incongruent
        plt.title(plotTitle)
        plt.savefig(plotFileName)
        plt.close()
        
        
plotIndividualLines(startDecade=1800, endDecade=2000, averaged=False, contextRelevant=True)