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

class FloridaSimSocres:
    def __init__(self):
        self.parsedLines = []
        self.simScores = {}
        self.highDifferencePairs = {}
        self.years = [1930, 1940, 1950, 1960, 1970, 1980, 1990]
    
    def parseFiles(self, origFile, writeFile):
        with open(origFile, "r") as data:
            for line in data:
                split = line.split(',')
                lineList = [split[0].lower(), split[1][1:].lower()]
                self.parsedLines.append(lineList)

        with open(writeFile, "w") as aFile:
            for line in self.parsedLines:
                lineStr = line[0] + " " + line[1] + "\n"
                aFile.write(lineStr)

    def findMaxDiff(self, simScores):
        longestIntervalDiff, maxDiff = 0, 0
        minIndex, minYear = 0, 0
        i = 0
        while simScores[i] == 0:
            i += 1
            if i >= len(simScores):
                return 0, 0
        minIndex = i
        minYear = self.years[i]
        longestIntervalDiff = simScores[-1] - simScores[minIndex]
        return longestIntervalDiff, minIndex

        # TODO: would be cool to also find the maximum interval that these scores are different
        

    def writeToOutput(self, timeSimIter, stim, word, fileName):
        allSimScores = []
        with open(fileName, "a") as resultFile:
            for year, sim in timeSimIter.iteritems():
                simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)
                outputStr = str(stim) + " " + str(word) + " " +  simStr + "\n"
                allSimScores.append(sim)
                resultFile.write(outputStr)
            resultFile.write("\n")
            difference, startYearIndex = self.findMaxDiff(allSimScores)
            if abs(difference) > .3:
                self.highDifferencePairs[(stim, word)] = (difference, startYearIndex)
            self.simScores[(stim, word)] = allSimScores
            

    def getSimScores(self, dataFile, resultFile):
        real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(1930, 1990, 10))
        for line in self.parsedLines:
            stim, word = line[0], line[1]
            timeSimIter = real_embeddings.get_time_sims(stim.lower(), word.lower())
            self.writeToOutput(timeSimIter, stim, word, resultFile)
            

florida = FloridaSimSocres()
florida.parseFiles("floridaData/gkPairs.txt", "floridaData/gkPairsPairsed.txt")
florida.getSimScores("floridaData/gkPairs.txt", "floridaResults/gkPairs.txt")
with open("floridaResults/gkPairsHighDiff.txt", "w") as f:
    for pair in florida.highDifferencePairs:
        difference, startYearIndex = florida.highDifferencePairs[pair]
        startYear = florida.years[startYearIndex]
        diffStr = pair[0] + ", " + pair[1] + " "  + str(startYear) + " " + str(florida.highDifferencePairs[pair][0]) + "\n"
        f.write(diffStr)
        




