# ------------------------------------------------------------------------- 
# * A Monte Carlo simulation of Galileo's three dice experiment. 
# * 
# * Name              : galileo.c 
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C
# * Latest Revision   : 9-11-98
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
# * ------------------------------------------------------------------------- 
# */


from rng import random, putSeed

N = 10000                          # number of replications */


def Equilikely(a,b):        
# # ------------------------------------------------
# * generate an Equilikely random variate, use a < b 
# * ------------------------------------------------
# */
  return (a + int((b - a + 1) * random()))




# i                               # replication index      */
# x                               # sum of three dice      */
count=[0 for i in range(0,19)]    # histogram              */
p=[0.0 for i in range(0,19)]      # probability estimates  */

putSeed(0)

for i in range(0,N): 
  x = Equilikely(1, 6) + Equilikely(1, 6) + Equilikely(1, 6)
  count[x] += 1

for x in range(3,19):             # estimate probabilities */
  p[x] = float(count[x]) / N

print("\nbased on {0:d} replications the estimated probabilities are:\n".format(N))
for x in range(3,19):
  print("p[{0:2d}] = {1:5.3f}".format(x, p[x]))


# C output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# based on 10000 replications the estimated probabilities are:

# p[ 3] = 0.004
# p[ 4] = 0.014
# p[ 5] = 0.030
# p[ 6] = 0.043
# p[ 7] = 0.066
# p[ 8] = 0.102
# p[ 9] = 0.119
# p[10] = 0.120
# p[11] = 0.125
# p[12] = 0.116
# p[13] = 0.095
# p[14] = 0.068
# p[15] = 0.047
# p[16] = 0.029
# p[17] = 0.016
# p[18] = 0.005