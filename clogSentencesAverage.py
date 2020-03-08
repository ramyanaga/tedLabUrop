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

sentenceContextWords = [
    # 'could not take message pencil paper',
    # 'caring hospitalized patients doctor help',
    # #'forgot utensils salad doctor went back get',
    # 'utensils salad',
    # 'little girl refused sleep',
    # #'grandchildren hired live-in nurse old live',
    # 'grandchildren hired nurse old live',
    # 'seen spider tangled own',
    # 'wrote note wouldnt',
    # 'prisoners planning',
    # 'winter house chimney puffs billowing',
    # #'giraffes long necks zebras',
    # 'zebras',
    # 'dinner guests eating appetizers another',
    # 'groom took brides hand placed ring',
    # 'little puppy grew huge'
    'father carved turkey',
    'added name',
    'felt sorry',
    'teacher students cheating wrote',
    'shut front window lock back',
    'show changed',
    'power went out house',
    'biking work driving',
    'dog good sense',
    'spend december 25th',
    'night old woman locked',
    'lightening heard',
    'movie baby started',
    'remember',
    'shouted top',
    'ringing busy cleaning chimney',
    'hurricane area window filled broken',
    'rude waiter',
    'dispute settled third',
    # 'careful top stove',
    # 'go bed turn off',
    # 'two met one held out his',
    # 'painted the clown suit build gave big red',
    # 'jumped lake made big',
    # 'bend elbow broken',
    # 'boss refused give',
    # 'call middle',
    # 'children outside',
    # 'fed baby warm',
    # 'schools closed teachers decided to go',
    # 'minutes arriving office detective spilled thermos full',
    # 'dirty dishes',
    # 'docked hour pay coming work',
    # 'afraid walk near edge cliff afraid',
    # 'not read well without',
    # 'shark attacks occur close',
    # 'everyone honking old man driving',
    # 'none books', # this seems like bad for context
    # 'mailed letter without',
    # 'cows moved from sun',
    # 'boys played marbles girls jumped',
    # 'knocked surfboard first',
    # 'threw rock broke',
    # 'spilled coffee clean white',
    # 'cold damp weather joints ache aspirin',
    # 'bottle of wine soft',
    # 'ship disappeared thick',
    # 'board window long',
    # 'weather warmer wearing lighter jacket heavy winter',
    # 'peral necklace',
    # 'pet',
    # 'smell tobacco'
]

sentenceContextWords = {
    'could not take message pencil piece': 'paper',
    'caring hospitalized patients doctor help': 'nurse',
    # #'forgot utensils salad doctor went back get': 'fork',
    # 'utensils salad': 'fork',
    # 'little girl refused sleep': 'story',
    # #'grandchildren hired live-in nurse old live': 'alone',
    # 'grandchildren hired nurse old live': 'alone',
    # 'seen spider tangled own': 'web',
    # 'wrote note wouldnt': 'forget,
    # 'prisoners planning': 'escape,
    # 'winter house chimney puffs billowing': 'smoke',
    # #'giraffes long necks zebras': 'stripes',
    # 'zebras': 'stripes',
    # 'dinner guests eating appetizers another': 'hour',
    # 'groom took brides hand placed ring': 'finger',
    # 'little puppy grew huge': 'dog'
    'father carved turkey': 'knife',
    'added name': 'list',
    'felt sorry': 'fault',
    'teacher students cheating wrote': 'names',
    'shut front window lock back': 'door',
    'show changed': 'channel',
    'power went out house': 'dark',
    'biking work driving': 'car',
    'dog good sense': 'smelly',
    'spend december 25th': 'family',
    'night old woman locked': 'door',
    'lightening heard': 'thunder',
    'movie baby started': 'cry',
    'remember': 'name',
    'shouted top': 'lungs',
    'ringing busy cleaning chimney': 'phone',
    'hurricane area window filled broken': 'glass',
    'rude waiter': 'tip',
    'dispute settled third': 'party',
    'careful top stove': 'hot',
    'go bed turn off': 'lights',
    'two met one held out his': 'hand',
    'painted the clown suit build gave big red': 'nose',
    'jumped lake made big': 'splash',
    'bend elbow broken': 'arm',
    'boss refused give': 'raise',
    'call middle': 'night',
    'children outside': 'play',
    'fed baby warm': 'milk',
    'schools closed teachers decided to go': 'strike',
    'minutes arriving office detective spilled thermos full': 'coffee',
    'dirty dishes': 'sink',
    'docked hour pay coming work': 'late',
    'afraid walk near edge cliff afraid': 'fall',
    'not read well without': 'glasses',
    'shark attacks occur close': 'shore',
    'everyone honking old man driving': 'slowly',
    'none books': 'sense', # this seems like bad for context
    'mailed letter without': 'stamp',
    'cows moved from sun': 'shade',
    'boys played marbles girls jumped': 'rope',
    'knocked surfboard first': 'wave',
    'threw rock broke': 'window',
    'spilled coffee clean white': 'shirt',
    'cold damp weather joints ache aspirin': 'pain',
    'bottle of wine soft': 'music',
    'ship disappeared thick': 'fog',
    'board window long': 'short',
    'weather warmer wearing lighter jacket heavy winter': 'coat',
    'peral necklace': 'birthday',
    'pet': 'leash',
    'smell tobacco': 'smoke',
    'time buy cake store change clothes guests': 'arrived',
    'cake guests': 'arrived',
    'squirrel stored nuts': 'tree',
    'morning school mother clothes packed': 'lunch',
    'touch wet': 'paint',
    'cats scratched': 'ears',
    'white gull dove caught': 'fish',
    'cold night': 'blanket',
    'refused changed': 'mind',
    'brightly colored picutres': 'wall',
    'clothes': "wear",
    'raised pigs': 'farm',
    'listen loud music door bedroom': 'open',
    'door bedroom': 'open',
    'skin red day': 'beach',
    'colonel wished seargeant treat command polite request': 'order',
    'command request': 'order',
    'shuffle cards': 'deal',
    'sword dangerous': 'sharp',
    'baby cried upset': 'mother',
    'baby': 'mother',
    'tenants landlord': 'court',
    'car knee bumper spare': 'key',
    'spare': 'key',
    'constructon worker powerful arms bags cement': 'truck',
    'cat curled': 'lap',
    'night campers built': 'fire',
    'sound system installed': 'car',
    'dinner spent time coffee': 'talking',
    'fertilizer enriched': 'soil',
    'problem cant take': 'joke',
    'positioned violin': 'chin',
    'clean sheet': 'bed',
    'buy small place build addition': 'rooms',
    'university register paid overdue fines': 'books',
    'pictures square plates': 'round',
    'plates': 'round',
    'national anthem': 'stand'
}




yearEmbeddingMap = {1940: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1940]),
                    1950: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1950]),
                    1960: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1960]),
                    1970: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1970]),
                    1980: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1980]),
                    1990: SequentialEmbedding.load("../embeddings/eng-all_sgns", [1990])}

def readFile():
    sentences = []
    highWords = []
    with open("CLOGSentences.txt") as f:
        for line in f:
            if len(line) > 2:
                sentences.append(line)
    with open("CLOGlastwords.txt") as f:
        for line in f:
            line.replace("'", "")
            line = line[:-1]
            lowercase = line.lower()
            #print("lowercase: ", lowercase)
            highWords.append(lowercase)
    return sentences, highWords


def phraseSimScores(stimWords, word):
    #real_embeddings = SequentialEmbedding.load("embeddings/eng-all_sgns", [1990])
    years = [1940, 1950, 1960, 1970, 1980, 1990]
    sims = []
    for year in years:
        real_embeddings = yearEmbeddingMap[year]
        stimWordVectors = []
        for sWord in stimWords:
            sEmbed = real_embeddings.get_subembeds([sWord])
            try:
                sEmbed.embeds[year].normalize()
            except ValueError:
                return 0
            sVec = sEmbed.embeds[year].m
            stimWordVectors.append(sVec)
        v_stack = np.vstack(tuple(stimWordVectors))
        mean_vector = np.mean(v_stack, axis=0).reshape((300, 1))

        wordEmbed = real_embeddings.get_subembeds([word])
        try:
            wordEmbed.embeds[year].normalize()
        except ValueError:
            return 0
        wordVec = wordEmbed.embeds[year].m
        sim = wordVec.dot(mean_vector)
        sims.append(sim[0, 0])
    return sum(sims)/len(sims)


def outputSimilarities():
    sentences, highWords = readFile()
    #real_embeddings = SequentialEmbedding.load("embeddings/eng-all_sgns", [1990])
    scores = []
    with open("clogSentencesAverageWords.txt", "w") as resultFile:
        for sentence in sentenceContextWords:
            split_sentence = sentence.split(' ')
            highWord = sentenceContextWords[sentence]
            simScore = phraseSimScores(split_sentence, highWord)
            scores.append(simScore)
            fileStr = sentence + ", " + highWord + " simScore: " + str(simScore) + "\n"
            resultFile.write(fileStr)
    
    x = [i for i in range(len(sentenceContextWords))]
    plt.xlabel("data point number")
    plt.ylabel("cosine similarity score")
    plt.title("Similarity score per clog sentence")
    plt.plot(x, scores)
    plt.show()
    plt.savefig("clogSentenceSimScores")

# This is junk, doesn't create sentence embeddings
# def outputSimilarities():
#     sentences, highWords = readFile()
#     embeddings = SequentialEmbedding.load("embeddings/eng-all_sgns", range(1940, 2000, 10))
    
#     with open("clogSentencesAverageWords.txt", "w") as resultFile:
#         #for i in range(len(highWords)):
#         for i in range(20):
#             yearSimAvg = {}
#             for year in range(1940, 2000, 10):
#                 yearSimAvg[year] = []
            
#             for j in range(len(sentenceContextWords[i])):
#                 sentence = sentenceContextWords[i][j]
#                 for word in sentence:
#                     time_sims = embeddings.get_time_sims(word, highWords[i])
#                     for year, sim in time_sims.iteritems():
#                         yearSimAvg[year].append(sim)
                
#             for yearKey in yearSimAvg:
#                 yearSimAvg[yearKey] = sum(yearSimAvg[yearKey])/len(yearSimAvg)
            
#             for year in yearSimAvg:
#                 avg = yearSimAvg[year]
#                 #simStr = "{year:d}, cosine_similarity={avg:0.2f}".format(year=year, sim=avg)
#                 simStr = "year " + str(year) + " cosine similarity= " + str(avg)
#                 strWithWords = sentenceContextWords[i] + " " + highWords[i] + " " + simStr
#                 resultFile.write(strWithWords)
#                 resultFile.write("\n")
#             resultFile.write("\n")

outputSimilarities()





