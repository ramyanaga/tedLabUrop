# tedLabUrop

To use the code in this repo:
1. Clone the histwords repo into a directory; you will need to follow the directions on the histwords
   github README to do this.
2. Clone this repo into the histwords repo
Your directory system should look like .../histwords/tedLabUrop after following the above two steps
(For example, my directory looks like ~/histwords/tedLabUrop)

## individualLineGraphs
Every file in this folder is a plot with 3 lines: a green line for the cosine similarity score
of (stimWord, high) over time, a red line for the cosine similarity score of (stimWord, low) over time, and
a magenta line for the cosine similarity score of (stimWord, incongruent) over time.

## averagedLineGraphs
Every file in this folder is a plot with 3 lines: a green line for the cosine similarity score
of (stimWord, high) averaged over time; this means that the cosine similarity score plotted
at the year 1950 is the average of the cosine similarity scores at years 1800 - 1950 (inclusive).

## contextRelevantLineGraphs
Every file in this folder is a plot with 3 lines: a green line for the context relevant score similarity
of (stimWord, high) over time, a red line for the context relevant similarity score of (stimWord, low) over time, and
a magenta line for the context relevant similarity score of (stimWord, incongruent) over time.
The context relevants score of a pair of words is defined as follows:

## stimWordIntervals
This folder has a number of bar graphs. Each bar graph in this folder has a bar for the average
cosine similarity score of (stim, high), (stim, low), and (stim, incongruent) pairs
in the year used in the bar plot label and the year 1990. For filenames with "_avg"
at the end, the values of the first three bars are calculated using the average
high/low/incongruent pair similarity score from that year through 1990. 
Ignore files named *_avg.png and *_avg.txt

## floridaResults
This folder has results from the florida norms dataset.
There are 2 types of files in this directory: <>.txt files and <>HighDiff.txt files.

The <>.txt file (for example abPairs.txt) has the similarity scores over time
of all words pairs in the florida norms data. The <>HighDiff.txt files
have the pairs that have changed by >= +/-.3 over time

## Recreating Plots
1. To re-create the line graphs in individualLineGraphs, averagedLineGraphs, and contextRelevantLineGraphs:

      a. create an empty directory named either individualLineGraphs, averagedLineGraphs, or contextRelevantLineGraphs (depending
          on which set of plots you are trying to re-create)

      b. modify the function call at the bottom of the file stimWordLineGraphs.py to one of the following:

         i. For individualLineGraphs:
         ```bash
            plotIndividualLines(startDecade=1800, endDecade=2000, False, False)
         ```

         ii. For averagedLineGraphs:
         ```bash
            plotIndividualLines(startDecade=1800, endDecade=2000, averaged=True, contextRelevant=False)
         ```

         iii. For contextRelevantGraphs:
         ```bash
            plotIndividualLines(startDecade=1800, endDecade=2000, averaged=False, contextRelevant=False)
         ```

      c. run the file stimWordLineGraphs.py

      d. Bonus: you can play around with the start or end decade by changing the function parameter to modify
      your graphs to start or end at different periods of time.
   
   2. To re-create the plot in the file changesInSimilarityScoresExtended.png run the file stimWordsAllLineGraphs.py
