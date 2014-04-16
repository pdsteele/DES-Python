# ---------------------------------------------------------------------- *
# * A Monte Carlo simulation to estimate the probability that the          *
# * determinant of a 3 by 3 matrix of random numbers is positive.          * 
# *                                                                        *
# * Name              : det.c                                              *
# * Author            : Larry Leemis                                       *
# * Language          : ANSI C                             
# * Latest Revision   : 8-8-02                                             *
# * Compile with      : gcc det.c rng.c                                    *
# *                     if math functions needed, add #include <math.h>    *
# *                     and compile with gcc -lm det.c rng.c  
#  # Translated by     : Philip Steele 
#  # Language          : Python 3.3
#  # Latest Revision   : 3/26/14             
#    Warning           : Reduce number of replications for python version
#                        to run quickly. Full 200000000 takes an hour or two
# * ---------------------------------------------------------------------- */

from rng import putSeed, random

N = 200000000                     # number of replications        */


#    i                              # replication index             */
#    j                              # row index                     */
#    k                              # column index                  */                        
#    temp1                          # first 2 by 2 determinant      */
#    temp2                          # second 2 by 2 determinant     */
#    temp3                          # third 2 by 2 determinant      */
#    x                              # determinant                   */

a = [[0 for i in range(0,4)] for i in range(0,4)]  # matrix (only 9 elements used) */
count = 0                      # counts number of pos det      */

putSeed(0)

for i in range(0,N):
  for j in range(1,4):
    for k in range(1,4):
      a[j][k] = random()
      if (j != k):
        a[j][k] = -a[j][k]
    #EndFor
  #EndFor
  temp1 = a[2][2] * a[3][3] - a[3][2] * a[2][3]
  temp2 = a[2][1] * a[3][3] - a[3][1] * a[2][3]
  temp3 = a[2][1] * a[3][2] - a[3][1] * a[2][2]
  x = a[1][1] * temp1 - a[1][2] * temp2 + a[1][3] * temp3
  if (x > 0):
    count += 1
#EndFor

print("\nbased on {0:1d} replications ".format(N))
print("the estimated probability of a positive determinant is:")
print("{0:11.9f}".format(float(count / N)))

#C output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# based on 200000000 replications the estimated probability of a positive determinant is:
# 0.050202725