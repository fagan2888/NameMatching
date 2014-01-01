
import csv
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import pylab

fn2 = "/Users/pgoldsmithpinkham/Dropbox/Papers/BenmelechStein/call_report_names_unique.csv"
reader = csv.reader(open(fn2,'rb'))
banknamesLong = [line[1].lower() for line in reader if line[2] != "rssd9348"]

uniqueLetters = [len(set(x)) for x in banknamesLong]
dupLetters = [len(x) - y for x, y in zip(banknamesLong, uniqueLetters)] 

n, bins, patches = plt.hist(uniqueLetters, 17, normed=1, facecolor='green', alpha=0.5, align="left")
plt.xlabel('Unique Num Letters')
plt.ylabel('Probability')
plt.title(r'Histogram of Unique Number of Letters in String')
pylab.savefig('uniqueNumLetters.pdf', bbox_inches=0)
plt.close()

n, bins, patches = plt.hist(dupLetters, max(dupLetters)-min(dupLetters), normed=1, facecolor='green', alpha=0.5, align="left")
plt.xlabel('Duplicate Num Letters')
plt.ylabel('Probability')
plt.title(r'Histogram of Duplicate Number of Letters in String')
pylab.savefig('duplicateNumLetters.pdf', bbox_inches=0)
plt.close()




#plt.show()
