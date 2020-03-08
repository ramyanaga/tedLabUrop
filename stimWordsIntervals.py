'''
This file calculates the similarity score between stim, high, low, incongruent words
over the ranges (1900, 2000), (1910, 2000), (1920, 2000), etc. through (1990, 2000)

TODO: Also play with moving the end interval backwards ie: (1900, 2000), (1900, 1990), etc.
'''
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

def computeAvgs(timeSimIterItems):
    long_sum, short_sum = 0, 0
    longAvgCount, shortAvgCount = 0, 0
    for year, sim in timeSimIterItems.iteritems():
        #print(year)
        long_sum += sim
        longAvgCount += 1
        if year >= 1980:
            shortAvgCount += 1
            short_sum += sim
    return long_sum/longAvgCount, short_sum/shortAvgCount


def writeToFile(timeSim, startYear, stimWord, correspondingWord):
    #fileName = "stimWordsIntervals/" + str(startYear) + ".txt"
    fileName = "stimWordsIntervals/" + str(startYear) + "_range.txt"
    with open(fileName, "a") as resultFile:
        for year, sim in timeSim.iteritems():
            simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)
            finalStr= str(stimWord) + " " + str(correspondingWord) + " " +  simStr + "\n"
            resultFile.write(finalStr)
        resultFile.write("\n")


# plot averages over the range(1900, 1990] against (1980, 1990]
def outputAndPlotSimilarities():
    wordPairsList = parseTxtFile()
    figureCount = 0
    highVal8090, lowVal8090, inconVal8090 = [], [], []
    base_embedding = SequentialEmbedding.load("../embeddings/eng-all_sgns", [1980, 1990])
    for wordList in wordPairsList:
        if len(wordList) < 4:
            continue
        stimWord = wordList[0]
        high, low, incongruent = wordList[1], wordList[2], wordList[3]
        time_sim_high = base_embedding.get_time_sims(stimWord, high)
        time_sim_low = base_embedding.get_time_sims(stimWord, low)
        time_sim_incon = base_embedding.get_time_sims(stimWord, incongruent)
        for sim_year, sim in time_sim_high.iteritems():
            #print("sim, sim_year: ", sim, sim_year)
            highVal8090.append(sim)
        for sim_year, sim in time_sim_low.iteritems():
            lowVal8090.append(sim)
        for sim_year, sim in time_sim_incon.iteritems():
            inconVal8090.append(sim)

    for year in [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980]:
        real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", [year, 1990])
        yearHighVals, yearLowVals, yearInconVals = [], [], []
        for wordList in wordPairsList:
            if len(wordList) < 4:
                continue
            stimWord = wordList[0]
            high, low, incongruent = wordList[1], wordList[2], wordList[3]
            time_sim_high = real_embeddings.get_time_sims(stimWord, high)
            time_sim_low = real_embeddings.get_time_sims(stimWord, low)
            time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

            for sim_year, sim in time_sim_high.iteritems():
                yearHighVals.append(sim)
            for sim_year, sim in time_sim_low.iteritems():
                yearLowVals.append(sim)
            for sim_year, sim in time_sim_incon.iteritems():
                yearInconVals.append(sim)
            
            writeToFile(time_sim_high, year, stimWord, high)
            writeToFile(time_sim_low, year, stimWord, low)
            writeToFile(time_sim_incon, year, stimWord, incongruent)

    
        nameEnd = "-1990"
        #barNames = (str(year) + nameEnd + "highBar", str(year) + nameEnd + "shortBar", str(year) + nameEnd + "inconBar",
        #                "1980-1990highBar", "1980-1990lowBar", "1980-1990inconBar")


        barNames = (str(year) + " high", str(year) + " low", str(year) + " incon",
                    "1990 high", "1990 low", "1990 incon")

        yearHighAvg = sum(yearHighVals)/len(yearHighVals)
        yearLowAvg = sum(yearLowVals)/len(yearLowVals)
        yearInconAvg = sum(yearInconVals)/len(yearInconVals)

        high8090Avg = sum(highVal8090)/len(highVal8090)
        low8090Avg = sum(lowVal8090)/len(lowVal8090)
        incon8090Avg = sum(inconVal8090)/len(inconVal8090)

        # with open("singleSimScores.txt", "a") as f:
        #     f.write(str(year) + ",1990 high average: " + str(yearHighAvg) + "\n")
        #     f.write(str(year) + ",1990 low average: " + str(yearLowAvg) + "\n")
        #     f.write(str(year) + ",1990 incongruent average: " + str(yearInconAvg) + "\n")
        #     f.write("1980, 1990 high average: " + str(high8090Avg) + "\n")
        #     f.write("1980 1990 low average: " + str(low8090Avg) + "\n")
        #     f.write("1980 1990 incongruent average " + str(incon8090Avg) + "\n")
        #     f.write("\n")

        barHeights = [yearHighAvg, yearLowAvg, yearInconAvg, 
                      high8090Avg, low8090Avg, incon8090Avg]
    
        
        print(barHeights)
        plt.figure(figureCount)
        plt.bar(barNames, barHeights)
        save_str = "stimWordsIntervals/" + str(year)
        plt.savefig(save_str)
        figureCount += 1

            
outputAndPlotSimilarities()


# change embedding loading to plot (1900, 1990] against (1980, 1990] (not the entire range, just those numbers)
# TODO: figure out + fix the weird recursion error
def outputAndPlotSimilaritiesRange():
    wordPairsList = parseTxtFile()
    for year in [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980]:
        highLongRangeVals, lowLongRangeVals, inconLongRangeVals = [], [], []
        highShortRangeVals, lowShortRangeVals, inconShortRangeVals = [], [], []
        wordCount = 0
        real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(year, 2000, 10))
        fileStr = "stimWordsIntervals/" + str(year) + "_range.txt"
        for wordList in wordPairsList:
            if len(wordList) < 4:
                continue
            wordCount += 1
            stimWord = wordList[0]
            high, low, incongruent = wordList[1], wordList[2], wordList[3]
            time_sim_high = real_embeddings.get_time_sims(stimWord, high)
            time_sim_low = real_embeddings.get_time_sims(stimWord, low)
            time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

            high_long_avg, high_short_avg = computeAvgs(time_sim_high)
            low_long_avg, low_short_avg = computeAvgs(time_sim_low)
            incon_long_avg, incon_short_avg = computeAvgs(time_sim_incon)

            # writeToFile(time_sim_high, year, stimWord, high)
            # writeToFile(time_sim_low, year, stimWord, low)
            # writeToFile(time_sim_incon, year, stimWord, incongruent)

            highLongRangeVals.append(high_long_avg)
            highShortRangeVals.append(high_short_avg)
            lowLongRangeVals.append(low_long_avg)
            lowShortRangeVals.append(low_short_avg)
            inconLongRangeVals.append(incon_long_avg)
            inconShortRangeVals.append(incon_short_avg)


            nameEnd = "-1990"
            barNames = (str(year) + " high", str(year) + " short", str(year) + " incon",
                        "1980-1990highBar", "1980-1990lowBar", "1980-1990inconBar")

            #print("sum: ", sum(highLongRangeVals))
            avg_high_long = sum(highLongRangeVals)/len(highLongRangeVals)
            avg_low_long = sum(lowLongRangeVals)/len(lowLongRangeVals)
            avg_incon_long = sum(inconLongRangeVals)/len(inconLongRangeVals)

            avg_high_short = sum(highShortRangeVals)/len(highShortRangeVals)
            avg_low_short = sum(lowShortRangeVals)/len(lowShortRangeVals)
            avg_incon_short = sum(inconShortRangeVals)/len(inconShortRangeVals)

            with open("stimWordsIntervals/rangeSimScores.txt", "a") as f:
                f.write(str(year) + ", 1990 high average: " + str(avg_high_long) + "\n")
                f.write(str(year) + ", 1990 low average: " + str(avg_low_long) + "\n")
                f.write(str(year) + ", 1990 incongruent average: " + str(avg_incon_long) + "\n")
                f.write("1980, 1990 high average: " + str(avg_high_short) + "\n")
                f.write("1980, 1990 low average: " + str(avg_low_short) + "\n")
                f.write("1980, 1990 incongruent average " + str(avg_incon_short) + "\n")
                f.write("\n")


            #barHeights = [avg_high_long, avg_low_long, avg_incon_long, 
            #              avg_high_short, avg_low_short, avg_incon_short]
            
            
            #plt.figure()
            #plt.bar(barNames, barHeights)
            #save_str = "stimWordsIntervals/" + str(year) + "_range"
            #plt.savefig(save_str)
            #figureCount += 1

#outputAndPlotSimilaritiesRange()