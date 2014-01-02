
import itertools
import csv
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import pylab
from collections import Counter
import time
from timer import Timer
from jellyfish import damerau_levenshtein_distance as ld

# This function finds the bins in binArray that are "close" to binVec, as
# defined by the threshold. It then returns those bins, and the strings that are 
# in those bins. (binVec and binArray need to be numpy arrays)
def compareBins(binVec, binArray, binDict, threshold=3):
    matchBins = list(binArray[np.sum(abs(binArray - binVec),1) <= threshold])
    matchStrings = list(itertools.chain.from_iterable(map(binDict.get, [tuple(x) for x in matchBins])))
    return (matchBins, matchStrings)

# Got this from here: https://wiki.python.org/moin/BitManipulation
# Adds up the number of bits that are "on"
def bitCount(int_type):
    count = 0
    while(int_type):
        int_type &= int_type - 1
        count += 1
    return(count)


def makeBinDict(stringList):
    binDict = {}
    for name in stringList:
        try:
            binDict[binCount(name,bins)].append(name)
        except KeyError:
            binDict[binCount(name,bins)] = [name]
    return binDict

def removeDuplicates(stringList):
    return list(set(stringList))

def makeBit(word, bitDict):
    return sum([bitDict[letter] for letter in set(word)])

def binCount(string,bins):
    stringCounter = Counter(string)
    coord = []
    for x,y in bins:
        #print LETTERS[x:y], sum([stringCounter[z] for z in LETTERS[x:y]])
        coord.append(sum([stringCounter[z] for z in LETTERS[x:y]]))
    return tuple(coord)

# Read in the two input files
fn = "bank_data.csv"
fn2 = "call_report_names_unique.csv"
with Timer() as t:
    with open(fn,'rb') as f:
        reader = csv.reader(f)
        banknamesShort = [line[2].lower() for line in reader if line[2] != "Bank_Name"]
    with open(fn2,'rb') as f:
        reader = csv.reader(f)
        banknamesLong = [line[1].lower() for line in reader if line[2] != "rssd9348"]

    banknamesLong = removeDuplicates(banknamesLong)
    banknamesShort = removeDuplicates(banknamesShort)
        
    #set of all letters used in strings
    LETTERS = list(set("".join(banknamesLong + banknamesShort)))
    
    #pick threshold
    threshold = 3

    #
    i = 0
    bins = []
    while i  < len(LETTERS):
        bins.append(tuple([i, i+7]))
        i = i + 7
    bitDict = {}
    i = 1
    for x in xrange(len(LETTERS)):
        bitDict[LETTERS[x]] = i
        i = i << 1

print "Startup Stage: %s seconds" % t.secs


with Timer() as t:
    binDictLong = makeBinDict(banknamesLong)
    binDictShort = makeBinDict(banknamesShort)
    
    binDictLongKeys = np.array(binDictLong.keys())
    binMatchesDict = {}
    nameMatchesDict = {}
    for keyShort in binDictShort.keys():
        (binMatches[keyShort], nameMatchesDict[keyShort]) = compareBins(np.array(keyShort), binDictLongKeys, binDictLong)
        

print "---------------------"
print "Bin Stage: %s seconds" % t.secs

# Use bitwise comparison to compare strings
counter = 0
successCounter = 0
compareDict = {}
with Timer() as t:
    for keyShort in binDictShort.keys():
        # Gets all words from the long list in the bins that
        # are in the ball close to the keyShort tuple.
        compareWords = nameMatchesDict[keyShort]
        # Make the comparison words into bit strings
        compareWordsBits = [makeBit(word2, bitDict) for word2 in compareWords]
        for shortWord in binDictShort[keyShort]:
            shortWordBits = makeBit(shortWord, bitDict)
            for i in range(len(compareWords)):
                if bitCount(shortWordBits ^ compareWordsBits[i]) <= threshold:
                    successCounter = successCounter + 1
                    try:
                        compareDict[shortWord].append(compareWords[i])
                    except KeyError:
                        compareDict[shortWord] = [compareWords[i]]
                    # print "Comparing %s and %s" % (shortWord, compareWords[i])
                    # print "Bit Representations:"
                    # print "%s" % (str(bin(shortWordBits))[2:])
                    # print "%s" % (str(bin(compareWordsBits[i]))[2:])
                    # print "Difference: %d" % bitCount(shortWordBits ^ compareWordsBits[i]) 
                counter = counter + 1

print "---------------------"
print "Bit Stage:  %s seconds" % t.secs
print "Number of Short Words: %d" % len(banknamesShort)
print "Number of Long Words: %d" % len(banknamesLong)
print "Theoretical Number of Matches (short x long): %d" % (len(banknamesShort) * len(banknamesLong))
print "Number of Total Comparisons: %d" % counter

matchCount =[]
with Timer() as t:
    for shortWord, compareWordsList in compareDict.items():
        compareVals = [ld(shortWord, longWord) for longWord in compareWordsList]
        minVal = min(compareVals)
        if minVal <= threshold:
            matches = [word for dist, word in zip(compareVals, compareWordsList) if dist == minVal]
            matchCount.append(len(matches))
            #matchString = ", ".join(matches)
            #print "Potential Matches for %s: %s, distance %d" % (shortWord, matchString, minVal)
        #else:
        #    print "No matches for %s" % shortWord

avgMatches = float(len(matchCount))/len(compareDict.keys())
fracMatched = float(len(matchCount))/len(banknamesShort)
print "---------------------"
print "LD Stage: %s seconds" % t.secs
print "Number of Comparisons: %d" % successCounter
print "Average Number of Matches: %f" % avgMatches
print "Fraction of Short Words w Match: %f" % fracMatched







    


