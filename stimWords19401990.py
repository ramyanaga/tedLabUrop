'''
from representations.sequentialembedding import SequentialEmbedding

"""
Example showing how to load a series of historical embeddings and compute similarities over time.
Warning that loading all the embeddings into main memory can take a lot of RAM
"""

if __name__ == "__main__":
    #fiction_embeddings = SequentialEmbedding.load("embeddings/eng-fiction-all_sgns", range(1950, 2000, 10))
    real_embeddings = SequentialEmbedding.load("embeddings/eng-all_sgns", range(1950, 2000, 10))
    #time_sims = fiction_embeddings.get_time_sims("lesbian", "gay")  
    time_sims = real_embeddings.get_time_sims("lesbian", "gay") 
    print("Similarity between gay and lesbian drastically increases from 1950s to the 1990s:")
    for year, sim in time_sims.iteritems():
        print("{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim))
'''
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

# dictionary mapping stimulus word to list of (high, low, incongruent)


multipleContentWords = ["musical instrument", "place live", "dairy product", 
                        "room house", "wild animal", "gardener tool", "farm animal",
                        "human body", "four footed animal", "room house", "kitchen tool", 
                        "four footed animal", "part bicycle", "musical instrument", 
                        "farm animal", "carpenter tool"]

multipleContentPairMap = {"musical instrument": ["drum", "banjo", "bolt"],
                          "place live": ["house, cabin, jelly"], 
                          "dairy product": ["milk", "cream", "gold"],
                          "thing read": ["book", "article", "warts"],
                          "room house": ["kitchen", "office", "monkey"], 
                          "wild animal": ["lion", "zebra", "acid"],
                          "gardener tool": ["shovel", "spade", "lunch"],
                          "farm animal": ["cow", "ox", "ivy"],
                          "human body": ["leg", "chest", "gyms"],
                          "place live": ["apartment", "tent", "domino"],
                          "four footed animal": ["cat", "pig", "bus"],
                          "part tree": ["branch", "twig", "plaza"],
                          "room house": ["bedroom", "attic", "brooms"],
                          "kitchen tool": ["fork", "mixer", "text"],
                          "four footed animal": ["dog", "mouse", "pink"],
                          "part bicycle": ["wheel", "lock", "store"],
                          "musical instrument": ["flute", "harp", "snap"],
                          "type bread": ["white", "french", "ruins"],
                          "room house": ["bathroom", "study", "zombie"],
                          "farm animal": ["pig", "mule", "pipe"],
                          "thing read": ["newspaper", "letter", "vulture"],
                          "carpenter tool": ["hammer", "ruler", "box"]}

yearEmbeddingMap = {1940: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1940]),
                    1950: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1950]),
                    1960: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1960]),
                    1970: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1970]),
                    1980: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1980]),
                    1990: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1990])}

# returns list of similarity scores for phrases from 1940 - 1990
#def phraseSimScoresOverTime(stimWords, word):


def phraseSimScores(stimWords, word, real_embeddings):
    stimWordVectors = []
    for sWord in stimWords:
        sEmbed = real_embeddings.get_subembeds([sWord])
        try:
            sEmbed.embeds[1990].normalize()
        except ValueError:
            return 0
        sVec = sEmbed.embeds[1990].m
        stimWordVectors.append(sVec)
    
    v_stack = np.vstack(tuple(stimWordVectors))
    mean_vector = np.mean(v_stack, axis=0).reshape((300, 1))
    
    wordEmbed = real_embeddings.get_subembeds([word])
    try:
        wordEmbed.embeds[1990].normalize()
    except ValueError:
        return 0
    wordVec = wordEmbed.embeds[1990].m
    sim = wordVec.dot(mean_vector)
    return sim[0, 0]

# used for words where mulitple words in the stim phrase are content words
def outputSimilaritiesAveraged():
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", [1990])
    with open("stimWordSimScores.txt", "a") as resultFile:
        for stimPhrase in multipleContentPairMap:
            stimWords = stimPhrase.split(' ')
            #stimWordEmbedding = real_embeddings.get_subembeds(stimWords)
            high, low, incon = multipleContentPairMap[stimPhrase]
            
            highSim = phraseSimScores(stimWords, high, real_embeddings)
            lowSim =  phraseSimScores(stimWords, low, real_embeddings) 
            inconSim =  phraseSimScores(stimWords, incon, real_embeddings)

            simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=1990,sim=float(highSim))
            highStr = str(stimPhrase) + " " + str(high) + " " +  simStr + "\n"
            resultFile.write(highStr)

            simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=1990,sim=float(lowSim))
            lowStr = str(stimPhrase) + " " +  str(low) +  " " + simStr + "\n"
            resultFile.write(lowStr)

            simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=1990,sim=float(inconSim))
            inconStr = str(stimPhrase) + " " + str(incon) + " " + simStr + "\n"
            resultFile.write(inconStr)
            resultFile.write("\n")
        
#outputSimilaritiesAveraged()


    
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
        

# this function used in cases where only one word in the stim word is a content word
def outputSimilarities():
    """
    outputs similarity scores between stim word, high, low, incongruent
    """
    wordPairsList = parseTxtFile()
    print(wordPairsList)
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", [1990])

    #with open("task1Results.txt", "w") as resultFile:
    with open("stimWordSimScores.txt", "w") as resultFile:
        for wordList in wordPairsList:
            if len(wordList) < 4:
                continue
            stimWord = wordList[0]
            high, low, incongruent = wordList[1], wordList[2], wordList[3]
            time_sim_high = real_embeddings.get_time_sims(stimWord, high)
            time_sim_low = real_embeddings.get_time_sims(stimWord, low)
            time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

            for year, sim in time_sim_high.iteritems():
                simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)
                highStr = str(stimWord) + " " + str(high) + " " +  simStr + "\n"
                resultFile.write(highStr)

            for year, sim in time_sim_low.iteritems():
                simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)
                lowStr = str(stimWord) + " " +  str(low) +  " " + simStr + "\n"
                resultFile.write(lowStr)
            
            for year, sim in time_sim_incon.iteritems():
                simStr = "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)
                inconStr = str(stimWord) + " " + str(incongruent) + " " + simStr + "\n"
                resultFile.write(inconStr)
            
            resultFile.write("\n")

#outputSimilarities()



'''
makes line graphs, where the green lines are
are (high, stim) over time, the red lines
are (low, stim) over time, and the magenta lines
are (incon, stim) over time

'''
def makeLineGraphs():
    wordPairsList = parseTxtFile()
    #real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(1940, 2000, 10))
    real_embeddings = SequentialEmbedding.load("../embeddings/eng-all_sgns", range(1800, 2000, 10))
    highPairs, lowPairs, inconPairs = {}, {}, {}
    key = 0

    for i in range(len(wordPairsList)):
        wordList = wordPairsList[i]
        if len(wordList) < 4:
            continue
        stimWord = wordList[0]
        high, low, incongruent = wordList[1], wordList[2], wordList[3]
        time_sim_high = real_embeddings.get_time_sims(stimWord, high)
        time_sim_low = real_embeddings.get_time_sims(stimWord, low)
        time_sim_incon = real_embeddings.get_time_sims(stimWord, incongruent)

        highPairs[i], lowPairs[i], inconPairs[i] = [], [], []

        for year, sim in time_sim_high.iteritems():
            print(year, sim)
            highPairs[i].append(sim)

        for year, sim in time_sim_low.iteritems():
            lowPairs[i].append(sim)
        
        for year, sim in time_sim_incon.iteritems():
            inconPairs[i].append(sim)
    
    # for stimPhrase in multipleContentPairMap:
    #     stimWords = stimPhrase.split(' ')
    #     high, low, incon = multipleContentPairMap[stimPhrase]



    mpl.style.use('default')
    
    # print(highPairs)

    highAvgs = [0 for i in range(1800, 2000, 10)]
    lowAvgs = [0 for i in range(1800, 2000, 10)]
    inconAvgs = [0 for i in range(1800, 2000, 10)]
    for i in range(len(highAvgs)):
        highIndexSum, lowIndexSum, inconIndexSum = 0, 0, 0
        for key in highPairs:
            highIndexSum += highPairs[key][i]
            lowIndexSum += lowPairs[key][i]
            inconIndexSum += inconPairs[key][i]
        highIndexAvg = highIndexSum/len(highPairs)
        lowIndexAvg = lowIndexSum/len(lowPairs)
        inconIndexAvg = inconIndexSum/len(inconPairs)
        highAvgs[i] = highIndexAvg
        lowAvgs[i] = lowIndexAvg
        inconAvgs[i] = inconIndexAvg
    
    years = [y for y in range(1800, 2000, 10)]
    

    for key in highPairs:
        plt.plot(years, highPairs[key], 'g')
    for key in lowPairs:
        plt.plot(years, lowPairs[key], 'r')
    for key in inconPairs:
        plt.plot(years, inconPairs[key], 'm')

    plt.plot(years, highAvgs, 'k', linewidth = 2.0)
    plt.plot(years, lowAvgs, 'k', linewidth=2.0)
    plt.plot(years, inconAvgs, 'k', linewidth=2.0)

    #plt.title("Changes in similarity scores over time")
    plt.title("Changes in similarity scores over time (extended)")
    plt.xlabel("Years")
    plt.ylabel("Similarity Scores")
    plt.show()

makeLineGraphs()
