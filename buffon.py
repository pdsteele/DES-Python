# -------------------------------------------------------------------------
# * A Monte Carlo simulation of Buffon's needle experiment. 
# * 
# * Name              : buffon.c 
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C
# * Latest Revision   : 9-11-98 
#   Translated by   : Philip Steele 
#   Language        : Python 3.3
#   Latest Revision : 3/26/14
# * ------------------------------------------------------------------------- 
# */

from rng import random, putSeed, getSeed
from math import cos, atan

N =      10000                      # number of replications */
HALF_PI =(2.0 * atan(1.0))          # 1.5707963...           */
R   =    1.0                        # length of the needle   */

def Uniform(a,b):  
# --------------------------------------------
# * generate a Uniform random variate, use a < b 
# * --------------------------------------------
# */
  return (a + (b - a) * random())  

################################Main Program#############################

putSeed(-1)                   # any negative integer will do      */
seed = getSeed()              # trap the value of the intial seed */
crosses = 0                   # tracks number of crosses

for i in range(0,N):                
  u     = random() #get first endpoint                                  
  theta = Uniform(-HALF_PI, HALF_PI) #get Angle
  v     = u + R * cos(theta) #get second endpoint
  if (v > 1.0):
    crosses += 1 #increase number of crosses


p = float(crosses / N)                # estimate the probability */

print("\nbased on {0:1d} replications and a needle of length {1:5.2f}".format(N, R))
print("with an initial seed of {0:1d}".format(seed))
print("the estimated probability of a cross is {0:5.3f}".format(p))

#C output:
# based on 10000 replications and a needle of length  1.00
# with an initial seed of 1396907952
# the estimated probability of a cross is 0.640