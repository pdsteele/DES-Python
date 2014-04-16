# # ---------------------------------------------------------------------- * 
#  * A Monte Carlo simulation of the hat check girl problem.                *
#  *                                                                        * 
#  * Name              : hat.c                                              * 
#  * Authors           : Steve Park & Dave Geyer                            * 
#  * Language          : ANSI C                                             * 
#  * Latest Revision   : 09-16-95                                           * 
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
#  * ---------------------------------------------------------------------- */

from rng import putSeed, random

# global variables */
#i                              # replication index         */
#arr                            # array                     */
count = 0                       # # of times a match occurs */
#p                              # probability estimate      */
SIZE = 10                       # array size                */
N = 10000                       # number of replications    */

def Equilikely(a,b):        
# # ------------------------------------------------
# * generate an Equilikely random variate, use a < b 
# * ------------------------------------------------
# */
  return (a + int((b - a + 1) * random()))


# ============================== */
def Initialize(a):
# ============================== */
  for j in range(0,SIZE):
    a[j] = j


# =========================== */
def Shuffle(a):
# =========================== */
  for j in range(0,SIZE-1):                 # shuffle an array         */
    t     = Equilikely(j, (SIZE - 1))       # in such a way that all   */
    hold  = a[j]                            # permutations are equally */
    a[j]  = a[t]                            # likely to occur          */
    a[t]  = hold

# ============================ */
def Check(a):
# ============================ */

  j    = 0
  test = 0
  condition = True

  while(condition==True):                   # test to see if at least */
    test = (a[j] == j)                      # one element is in its   */
    j += 1                                  # 'natural' position      */
    condition = (j != SIZE) and (test==0)   # - return a 1 if so      */
                                            # - return a 0 otherwise  */
  if (test == 1):
    return(1)
  else:
    return(0)


###############################Main Program##############################
putSeed(0)
arr = [None for i in range(0,SIZE)]
Initialize(arr)

for i in range(0,N):                 # do N Monte Carlo replications */
  Shuffle(arr)
  count += Check(arr)


p = float(N - count) / N             # estimate the probability */

print("\nfor {0:1d} replications and an array of size {1:d}".format(N, SIZE))
print("the estimated probability is {0:5.3f}".format(p))

# c output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# for 10000 replications and an array of size 10
# the estimated probability is 0.369
