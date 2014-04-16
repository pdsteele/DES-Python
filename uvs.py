# -------------------------------------------------------------------------  
# * This program reads a (text) data file and computes the mean, minimum, 
# * maximum, and standard deviation.   The one-pass algorithm used is due to 
# * B.P. Welford (Technometrics, vol. 4, no 3, August 1962.) 
# *
# * NOTE: the text data file is assumed to be in a one-value-per-line format
# * with NO blank lines in the file.   The data can be either fixed point 
# * (integer valued), or floating point (real valued). 
# *
# * To use the program, compile it to disk to produce uvs.  Then at a command 
# * line prompt, uvs can be used in three ways. 
# *
# * (1) To have uvs read a disk data file, say uvs.dat (in the format above),
# * at a command line prompt use '<' redirection as: 
# *
# *     python uvs < uvs.dat  
# *
# * (2) To have uvs filter the numerical output of a program, say test, at a
# * command line prompt use '|' pipe as: 
# *
# *     cat uvs.dat | python uvs.py (best way for Powershell,cmd)
# *
# * (3) To use uvs with keyboard input, at a command line prompt enter:
# *
# *      uvs
# *
# * Then enter the data -- one value per line -- being sure to remember to
# * signify an end-of-file.  In Unix/Linux, signify an end-of-file by
# * entering ^d (Ctrl-d) as the last line of input.
# * 
# * Name              : uvs.c  (Univariate Statistics)
# * Authors           : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 9-28-98
#  # Translated by    : Philip Steele 
#  # Language         : Python 3.3
#  # Latest Revision  : 3/26/14
# * ------------------------------------------------------------------------- 
# */

#include <stdio.h>                             
#include <math.h>  

from math import sqrt   
import sys                           



# long    index
# double  data
sum = 0.0
# double  mean
# double  stdev
# double  min
# double  max
# double  diff

data = sys.stdin.readline()

if (data):
  data = float(data)
  index  = 1
  mean   = data
  min    = data
  max    = data
else: 
  index = 0

data = sys.stdin.readline()
while (data):
  data = float(data)
  index += 1
  diff  = data - mean
  sum  += diff * diff * (index - 1.0) / index
  mean += diff / index
  if (data > max):
    max = data
  elif (data < min):
    min = data

  data = sys.stdin.readline()
#EndWhile

if (index > 0):
  stdev = sqrt(sum / index)
  print("\nfor a sample of size {0:d}".format(index))
  print("mean ................. = {0:7.3f}".format(mean))
  print("standard deviation ... = {0:7.3f}".format(stdev))
  print("minimum .............. = {0:7.3f}".format(min))
  print("maximum .............. = {0:7.3f}".format(max))




# C output:
# for a sample of size 1000
# mean ................. =   3.042
# standard deviation ... =   1.693
# minimum .............. =   0.207
# maximum .............. =  11.219
