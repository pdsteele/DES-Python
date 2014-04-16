# ----------------------------------------------------------------------
# * This program reads a data sample from a text file in the format
# *                         one data point per line 
# * and calculates an interval estimate for the mean of that (unknown) much 
# * larger set of data from which this sample was drawn.  The data can be 
# * either discrete or continuous.  A compiled version of this program 
# * supports redirection and can used just like program uvs.c. 
# * 
# * Name              : estimate.c  (Interval Estimation) 
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 11-16-98 
#  # Translated by     : Philip Steele 
#  # Language          : Python 3.3
#  # Latest Revision   : 3/26/14
# * ----------------------------------------------------------------------
# */

from rvms import idfStudent
from math import sqrt
import sys

LOC = 0.95                             # level of confidence,        */ 
                                       # use 0.95 for 95% confidence */


n    = 0                     # counts data points */
sum  = 0.0
mean = 0.0
# double data
# double stdev
# double u, t, w
# double diff

data = sys.stdin.readline()

while (data):                         # use Welford's one-pass method */                                    
  n += 1                              # to calculate the sample mean  */   
  diff  = float(data) - mean          # and standard deviation        */
  sum  += diff * diff * (n - 1.0) / n
  mean += diff / n
  data = sys.stdin.readline()
#EndWhile
stdev  = sqrt(sum / n)

if (n > 1): 
  u = 1.0 - 0.5 * (1.0 - LOC)              # interval parameter  */
  t = idfStudent(n - 1, u)                 # critical value of t */
  w = t * stdev / sqrt(n - 1)              # interval half width */
  print("\nbased upon {0:1d} data points and with {1:d} confidence".format(n,int(100.0 * LOC + 0.5)))
  print("the expected value is in the interval {0:10.2f} +/- {1:6.2f}".format(mean, w))

else:
  print("ERROR - insufficient data\n")

# C output:
# bash.exe"-3.1$ ./estimate.exe < uvs.dat

# based upon 1000 data points and with 95% confidence
# the expected value is in the interval      3.04 +/-   0.11