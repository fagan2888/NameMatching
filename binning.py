
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

# Got this from here: https://wiki.python.org/moin/BitManipulation
# Adds up the number of bits that are "on"
def bitCount(int_type):
    count = 0
    while(int_type):
        int_type &= int_type - 1
        count += 1
    return(count)

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


binDictLong = {}
binDictShort = {}
with Timer() as t:
    for name in banknamesLong:
        try:
            binDictLong[binCount(name,bins)].append(name)
        except KeyError:
            binDictLong[binCount(name,bins)] = [name]
    for name in banknamesShort:
        try:
            binDictShort[binCount(name,bins)].append(name)
        except KeyError:
            binDictShort[binCount(name,bins)] = [name]

    binDictLongKeys = np.array(binDictLong.keys())
    binMatches = {}
    nameMatchLen = {}
    for keyShort in binDictShort.keys():
        binMatches[keyShort] = list(binDictLongKeys[np.sum(abs(binDictLongKeys - np.array(keyShort)),1) <= threshold])
        nameMatchLen[keyShort] = len(list(itertools.chain.from_iterable(map(binDictLong.get, [tuple(x) for x in binMatches[keyShort]]))))

print "Bin Stage: %s seconds" % t.secs

# Use bitwise comparison to compare strings
counter = 0
successCounter = 0
with Timer() as t:
    for keyShort in binDictShort.keys():
        # Gets all words from the long list in the bins that
        # are in the ball close to the keyShort tuple.
        compareWords = list(itertools.chain.from_iterable(map(binDictLong.get, [tuple(x) for x in binMatches[keyShort]])))
        # Make the comparison words into bit strings
        compareWordsBits = [makeBit(word2, bitDict) for word2 in compareWords]
        for shortWord in binDictShort[keyShort]:
            shortWordBits = makeBit(shortWord, bitDict)
            for i in range(len(compareWords)):
                if bitCount(shortWordBits ^ compareWordsBits[i]) <= threshold:
                    successCounter = successCounter + 1
                    # print "Comparing %s and %s" % (shortWord, compareWords[i])
                    # print "Bit Representations:"
                    # print "%s" % (str(bin(shortWordBits))[2:])
                    # print "%s" % (str(bin(compareWordsBits[i]))[2:])
                    # print "Difference: %d" % bitCount(shortWordBits ^ compareWordsBits[i]) 
                counter = counter + 1


print "Bit Stage:  %s seconds" % t.secs
print "Number of Short Words: %d" % len(banknamesShort)
print "Number of Long Words: %d" % len(banknamesLong)
print "Theoretical Number of Matches (short x long): %d" % (len(banknamesShort) * len(banknamesLong))
print "Number of Total Comparisons: %d" % counter
print "Number of Potential Matches: %d" % successCounter








    


