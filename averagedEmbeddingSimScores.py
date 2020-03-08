import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from representations.sequentialembedding import SequentialEmbedding
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import csv
import numpy as np



# this uses the average embeddings of each stim word
# and high, low, incon word to calculate the similarity score as
# opposed to the using the average of similarity scores calculated
# over time

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

# def outputSimilaritiesAveraged():
#     embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(1940, 1990))
#     embeddings.


def getResultStr(stimWord, otherWord, startYear, endYear, sim):
    simStr = "cosine similarity={sim:0.2f}".format(sim=sim)
    return (stimWord + " " + otherWord + " " + str(startYear) + " " + str(endYear) + " " + simStr + "\n")

def getAveragedEmbedding(subembeds, startYear, endYear):
    averaged_embed_vec = np.zeros((1, 300))
    for year in range(startYear, endYear, 10):
        year_embed_vec = subembeds.embeds[year].m
        try:
            averaged_embed_vec += year_embed_vec
        except ValueError:
            print("in value error")
            return np.zeros((1, 300))
    averaged_embed_vec = averaged_embed_vec/((endYear - startYear)/10)
    return averaged_embed_vec

def getSimScore(embedding1, embedding2):
    sim = np.dot(embedding1, embedding2.T)
    return sim[0][0]

def outputSimilaritiesAveraged():
    wordPairsList = parseTxtFile()
    startYear, endYear = 1900, 1990
    embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(startYear, endYear, 10))

    highVals, lowVals, inconVals = [], [], []
    with open("stimWordsIntervals/" + str(startYear) + "_avg.txt", "a") as resultFile:
        for wordList in wordPairsList:
            if len(wordList) < 4:
                continue
            stimWord = wordList[0]
            high, low, incon = wordList[1], wordList[2], wordList[3]
            stimWordSubembeds = embeddings.get_subembeds([stimWord])
            highWordSubembeds = embeddings.get_subembeds([high])
            lowWordSubembeds = embeddings.get_subembeds([low])
            inconWordSubembeds = embeddings.get_subembeds([incon])
            
            stimWordAvgEmbed = getAveragedEmbedding(stimWordSubembeds, startYear, endYear)
            highAvgEmbed = getAveragedEmbedding(highWordSubembeds, startYear, endYear)
            lowAvgEmbed = getAveragedEmbedding(lowWordSubembeds, startYear, endYear)
            inconAvgEmbed = getAveragedEmbedding(inconWordSubembeds, startYear, endYear)

            highSim = getSimScore(stimWordAvgEmbed, highAvgEmbed)
            lowSim = getSimScore(stimWordAvgEmbed, lowAvgEmbed)
            inconSim = getSimScore(stimWordAvgEmbed, inconAvgEmbed)

            highVals.append(highSim)
            lowVals.append(lowSim)
            inconVals.append(inconSim)

            resultFile.write(getResultStr(stimWord, high, startYear, endYear, highSim))
            resultFile.write(getResultStr(stimWord, low, startYear, endYear, lowSim))
            resultFile.write(getResultStr(stimWord, incon, startYear, endYear, inconSim))
            resultFile.write("\n")

            barHeights = [sum(highVals)/len(highVals), sum(lowVals)/len(lowVals), sum(inconVals)/len(inconVals)]
            barNames = ["1900 high", "1900 low", "1900 incon"]
            plt.bar(barNames, barHeights, color='blue')
            save_str = "stimWordsIntervals/" + str(startYear) + "_avg.png"
            plt.figure(0)
            plt.savefig(save_str)

            #stimWordEmbedding = getAveragedEmbedding(stimWord)
            #highEmbedding, lowEmbedding, inconEmbedding = getAveragedEmbedding(high), getAveragedEmbedding(low), getAveragedEmbedding(incon)


outputSimilaritiesAveraged()
# subembeds = embeddings.get_subembeds(["hi"])
# averaged_embed_vec = np.zeros((1, 300))
# for year in range(1940, 1990, 10):
#     year_embed_vec = subembeds.embeds[year].m
#     averaged_embed_vec += year_embed_vec

# averaged_embed_vec = averaged_embed_vec/((1990 - 1940)/10)