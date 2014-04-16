# ------------------------------------------------------------------------- 
# * This program reads data from a text file and computes the mean, 
# * standard deviation, minimum, maximum, correlation coefficient and  
# * regression line angle (theta). 
# *  
# * NOTE: the text data file is assumed to be in a two-values-per-line format
# * (i.e. format) with NO blank lines in the file. 
# *
# * NOTE: for more information relative to the use of this program, see the
# * header of the analogous univariate program uvs.c 
# *
# * Name              : bvs.c (BiVariate Statistics) 
# * Authors           : Steve Park & Dave Geyer 
# * Language          : ANSI C  
# * Latest Revision   : 5-2-99
# * Compile with      : gcc -lm bvs.c
# * Execute with      : a.out < bvs.dat
#   Language          : Python 3.3
#   Latest Revision   : 3/26/14
#   Execute with      : python bvs.py < bvs.dat
# * ------------------------------------------------------------------------- 
# */

from math import atan, atan2, sqrt
import sys

class bivariate:
  def __init__(self,*args, **kwargs):
    try: #attempt to assign optional args 
      self.u = kwargs['u']
      self.v = kwargs['v'] 
    except:
      self.u = None
      self.v = None

def readNext(data):
  temp = sys.stdin.readline()
  if(temp):
    data.u = int(temp.split('  ')[0])
    data.v = int(temp.split('  ')[1])
  return (temp)


data = bivariate()
sum = bivariate(u=0.0,v=0.0)
mean = bivariate()
stdev = bivariate()
min = bivariate()
max = bivariate()
diff = bivariate()
cosum = 0.0
pi = 4.0 * atan(1.0)        # 3.14159 ... */


line = readNext(data)

if (line):
  index = 1
  mean.u  = data.u
  mean.v = data.v
  min.u  = data.u
  min.v = data.v
  max.u   = data.u
  max.v = data.v
else:
  index = 0

line = readNext(data)

while (line):
  index += 1
  temp    = (index - 1.0) / index
  diff.u  = data.u - mean.u
  diff.v  = data.v - mean.v
  sum.u  += diff.u * diff.u * temp
  sum.v  += diff.v * diff.v * temp
  cosum  += diff.u * diff.v * temp
  mean.u += diff.u / index
  mean.v += diff.v / index
  if (data.u > max.u):
    max.u = data.u
  elif (data.u < min.u):
    min.u = data.u

  if (data.v > max.v):
    max.v = data.v
  elif (data.v < min.v):
    min.v = data.v

  line = readNext(data)
#EndWhile


if (index > 0):
  stdev.u    = sqrt(sum.u / index)
  stdev.v    = sqrt(sum.v / index)
  covariance = cosum / index
  if (stdev.u * stdev.v > 0.0):
    correlation = covariance / (stdev.u * stdev.v)
  else:
    correlation = 0.0
  sum.u = stdev.u * stdev.u - stdev.v * stdev.v
  sum.v = 2.0 * covariance
  theta = 0.5 * atan2(sum.v, sum.u)
  print("\nfor a sample of size {0:1d}\n".format(index))
  print("mean.u ...... = {0:7.3f}".format(mean.u))
  print("stdev.u ..... = {0:7.3f}".format(stdev.u))
  print("min.u ....... = {0:7.3f}".format(min.u))
  print("max.u ....... = {0:7.3f}".format(max.u))
  print("mean.v ...... = {0:7.3f}".format(mean.v))
  print("stdev.v ..... = {0:7.3f}".format(stdev.v))
  print("min.v ....... = {0:7.3f}".format(min.v))
  print("max.v ....... = {0:7.3f}".format(max.v))
  print("correlation ...... = {0:7.3f}".format(correlation))
  print("theta (radians) .. = {0:7.3f}".format(theta))
  print("theta (degrees) .. = {0:7.3f}".format(180.0 * theta / pi))


# C output:
# for a bivariate sample of size 82

# mean.u ...... = 486.707
# stdev.u ..... = 101.153
# min.u ....... = 290.000
# max.u ....... = 730.000

# mean.v ...... = 610.988
# stdev.v ..... =  26.530
# min.v ....... = 520.000
# max.v ....... = 663.000

# correlation ...... =   0.590
# theta (radians) .. =   0.160
# theta (degrees) .. =   9.186