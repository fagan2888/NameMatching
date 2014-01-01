
import itertools
import csv
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import pylab
from collections import Counter

LETTERS = ["a", "b", "c", "d", "e",
           "f", "g", "h", "i", "j",
           "k", "l", "m", "n", "o",
           "p", "q", "r", "s", "t",
           "u", "v", "w", "x", "y", "z", " "]


# Pseudo-Code:
# "bins" will define the slices on the LETTERS list
# 1. Given a binning, for any string, create a tuple with the count in each bin (O(n))
# 2. Given counts, create a dict with counts as key, and list of strings as values
# 3. For each key, create list of possible comparison group keys
# 4. For each word, return the number of possible comparisons

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

fn = "/Users/pgoldsmithpinkham/Dropbox/Papers/BenmelechStein/bank_data.csv"
with open(fn,'rb') as f:
    reader = csv.reader(f)
    banknamesShort = [line[2].lower() for line in reader if line[2] != "Bank_Name"]
fn2 = "/Users/pgoldsmithpinkham/Dropbox/Papers/BenmelechStein/call_report_names_unique.csv"
with open(fn2,'rb') as f:
    reader = csv.reader(f)
    banknamesLong = [line[1].lower() for line in reader if line[2] != "rssd9348"]

banknamesLong = removeDuplicates(banknamesLong)
banknamesShort = removeDuplicates(banknamesShort)

LETTERS = list(set("".join(banknamesLong + banknamesShort)))

i = 0
bins = []
while i  < len(LETTERS):
    bins.append(tuple([i, i+7]))
    i = i + 7

binDictLong = {}
binDictShort = {}
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

threshold = 3

binDictLongKeys = np.array(binDictLong.keys())
binMatches = {}
nameMatchLen = {}
for keyShort in binDictShort.keys():
    binMatches[keyShort] = list(binDictLongKeys[np.sum(abs(binDictLongKeys - np.array(keyShort)),1) <= threshold])
    #print len(binMatches[keyShort])
    nameMatchLen[keyShort] = len(list(itertools.chain.from_iterable(map(binDictLong.get, [tuple(x) for x in binMatches[keyShort]]))))


matches = nameMatchLen.values()
n, bins, patches = plt.hist(matches, max(matches)-min(matches), normed=1, facecolor='green', alpha=0.5, align="left")            
pylab.savefig('numStringMatches.pdf', bbox_inches=0)
plt.close()

bitDict = {}
i = 1
for x in xrange(len(LETTERS)):
    bitDict[LETTERS[x]] = i
    i = i << 1


testword = binDictShort[keyShort][0]

compareWords = list(itertools.chain.from_iterable(map(binDictLong.get, [tuple(x) for x in binMatches[keyShort]])))

for word2 in compareWords:
    print bin(makeBit(testword, bitDict) ^ makeBit(word2, bitDict))
    #print word, word2




    


