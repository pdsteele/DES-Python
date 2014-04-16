# ------------------------------------------------------------------------- * 
# * A Monte Carlo simulation of the dice game Craps.                          * 
# *                                                                           * 
# * Name              : craps.c                                               * 
# * Author            : Steve Park & Dave Geyer                               * 
# * Language          : ANSI C                                                * 
# * Latest Revision   : 9-16-95                                               * 
# * Compile with      : gcc craps.c rng.c                                     *
#   Translated by     : Philip Steele 
#   Language          : Python 3.3
#   Latest Revision   : 3/26/14
 # * ------------------------------------------------------------------------- */

from rng import putSeed, random

N = 10000                           # number of replications */

# global variables */
# long    i                                 # replication index    */
# long    point                             # the initial roll     */
# long    result                            # 0 = lose, 1 = win    */
wins = 0                          # number of wins       */
# double  p                                 # probability estimate */

# ============================== */
def Equilikely(a,b):          # use a < b */
# ============================== */
  return(a + int((b - a + 1) * random()))


# ============== */
def Roll():
# ============== */
  return(Equilikely(1, 6) + Equilikely(1, 6))

# ==================== */                 # roll until a 7 is obtained */
def Play(point):                    #  - then return a 0         */
# ==================== */                 # or the point is made       */                                          
                                          #  - then return a 1         */                                      
  condition = True                                               
  while(condition == True):                                          
    sum = Roll()
    condition = (sum != point) and (sum != 7)

  if(sum == point):
    return(1)
  else:
    return(0)

############################Main Program#################################
putSeed(0)

for i in range(0,N):           # do N Monte Carlo replications */
  point = Roll() 
  if(point in [7,11]):
    result = 1
  elif(point in [2,3,12]):
    result = 0
  else:
    result = Play(point)

  wins += result
#EndFor

p =  float(wins) / float(N)          # estimate the probability */

print("\nfor {0:1d} replications".format(N))
print("the estimated probability of winning is {0:5.3f}\n".format(p))

# C output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# for 10000 replications
# the estimated probability of winning is 0.485