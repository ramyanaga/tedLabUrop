# tedLabUrop

To use the code in this repo:
1. Clone the histwords repo into a directory; you will need to follow the directions on the histwords
   github README to do this.
2. Clone this repo into the histwords repo
Your directory system should look like .../histwords/tedLabUrop after following the above two steps
(For example, my directory looks like ~/histwords/tedLabUrop)

## averagedLineGraphs
This folder has a plot with 3 line graphs: (stimWord, high), (stimWord, low), (stimWord, incongruent)
averaged over time. This means that the plotted similarity score for one of the lines
at the year 1950, is the average of similarity scores prior to and including the 1950s.
There is one plot per word triplet. \\
To re-create these graphs, run the stimWordLineGraphs.py file.
To run:
python stimWordLineGraphs.py

## floridaResults
This folder has results from the florida norms dataset.
There are 2 types of files in this directory: <>.txt files and <>HighDiff.txt files.
The <>.txt file (for example abPairs.txt) has the similarity scores over time
of all words pairs in the florida norms data. The <>HighDiff.txt files
have the pairs that have changed by >= +/-.3 over time

## stimWordIntervals
This folder has a number of bar graphs. Each bar graph in this folder has a bar for the average
cosine similarity score of (stim, high), (stim, low), and (stim, incongruent) pairs
in the year used in the bar plot label and the year 1990. For filenames with "_avg"
at the end, the values of the first three bars are calculated using the average
high/low/incongruent pair similarity score from that year through 1990. 
Ignore files named *_avg.png and *_avg.txt

