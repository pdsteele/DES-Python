# ------------------------------------------------------------------------
# * This program illustrates an array-based algorithm for tallying a 
# * continuous-data histogram for data read from standard input (stdin).
# * Like program uvs, a compiled version of this program supports file
# * redirection.
# *
# * The MIN, MAX, K parameters are "tuned" to the datafile uvs.dat.
# * For other datafiles these parameters must be adjusted -- you might
# * want to process the datafile with program uvs first to get a handle on
# * appropriate values for these three parameters.
# * 
# *  Name              : cdh.c  (Continuous Data Histogram)
# *  Authors           : Steve Park & Dave Geyer
# *  Language          : ANSI C
# *  Latest Revision   : 12-27-95
#  # Translated by     : Philip Steele 
#  # Language          : Python 3.3
#  # Latest Revision   : 3/26/14
#  * Execute with      : python cdh.py < uvs.dat
 # * ------------------------------------------------------------------------ 
 # */


from math import sqrt
import sys

MIN =    0.0
MAX =    8.0
K   =    16                          # number of histogram bins   */
DELTA =  ((MAX - MIN) / K)           # histogram bin size (width) */

def sqr(x):
  return ((x) * (x))

class outlie:
  lo = 0
  hi = 0

#################################Main Program###########################

index    = 0                                    # sample size         */
count=[0.0 for i in range(0,K)]                 # bin count           */
midpoint = []                                   # bin midpoint        */
outliers      = outlie()
sum      = 0.0
sumsqr   = 0.0


for j in range(0,K): 
  midpoint.append(MIN + (j + 0.5) * DELTA)

x = sys.stdin.readline()   #get data value

while (x):
  x = float(x)                                       # tally the data */
  index += 1
  if (x >= MIN) and (x < MAX):
    j = int((x - MIN) / DELTA)
    count[j] += 1  #j acts as histogram bin index
  elif (x < MIN):
    outliers.lo += 1
  else:
    outliers.hi += 1

  x = sys.stdin.readline()
#EndWhile

for j in range(0,K):                            # histogram mean */
  sum += midpoint[j] * count[j]
#EndFor 
mean   = sum / index

for j in range(0,K):                            # histogram stdev */
  sumsqr += sqr(midpoint[j] - mean) * count[j]
#EndFor
stdev     = sqrt(sumsqr / index)

print("  bin     midpoint     count   proportion    density\n")
for j in range(0,K): 
  print("{0:5d}".format(j + 1), end="")                         # bin        */
  print("{0:12.3f}".format(midpoint[j]), end="")                # midpoint   */
  print("{0:10d}".format(int(count[j])), end="")                # count      */
  print("{0:12.3f}".format(float(count[j] / index)), end="")    # proportion */
  print("{0:12.3f}".format(float(count[j] / (index * DELTA))))  # density    */

print("\nsample size .... = {0:7d}".format(index))
print("mean ........... = {0:7.3f}".format(mean))
print("stdev .......... = {0:7.3f}".format(stdev))
if (outliers.lo > 0):
  print("NOTE: there were {0:1d} low outliers".format(outliers.lo))
if (outliers.hi > 0):
  print("NOTE: there were {0:1d} high outliers".format(outliers.hi))

# C output:
#   bin     midpoint     count   proportion    density

#     1       0.250        11       0.011       0.022
#     2       0.750        53       0.053       0.106
#     3       1.250       109       0.109       0.218
#     4       1.750       142       0.142       0.284
#     5       2.250       120       0.120       0.240
#     6       2.750       133       0.133       0.266
#     7       3.250       112       0.112       0.224
#     8       3.750        69       0.069       0.138
#     9       4.250        78       0.078       0.156
#    10       4.750        42       0.042       0.084
#    11       5.250        34       0.034       0.068
#    12       5.750        28       0.028       0.056
#    13       6.250        21       0.021       0.042
#    14       6.750        20       0.020       0.040
#    15       7.250         9       0.009       0.018
#    16       7.750        12       0.012       0.024

# sample size .... =    1000
# mean ........... =   2.981
# stdev .......... =   1.612

# NOTE: there were 7 high outliers
