# -------------------------------------------------------------------------
# * This is an Java library for random number generation.  The use of this
# * library is recommended as a replacement for the Java class Random,
# * particularly in simulation applications where the statistical
# * 'goodness' of the random number generator is important.
# *
# * The generator used in this library is a so-called 'Lehmer random number
# * generator' which returns a pseudo-random number uniformly distributed
# * between 0.0 and 1.0.  The period is (m - 1) where m = 2,147,483,647 and
# * the smallest and largest possible values are (1 / m) and 1 - (1 / m)
# * respectively.  For more details see:
# *
# *       "Random Number Generators: Good Ones Are Hard To Find"
# *                   Steve Park and Keith Miller
# *              Communications of the ACM, October 1988
# *
# * Note that as of 7-11-90 the multiplier used in this library has changed
# * from the previous "minimal standard" 16807 to a new value of 48271.  To
# * use this library in its old (16807) form change the constants MULTIPLIER
# * and CHECK as indicated in the comments.
# *
# * Name              : Rng.java  (Random Number Generation - Single Stream)
# * Authors           : Steve Park & Dave Geyer
# * Translated by     : Philip Steele 
# * Language          : Python 3.3
# * Latest Revision   : 3/26/14
# *
# * Program rng       : Section 2.2
# * ------------------------------------------------------------------------- 
# */

from time import time

CHECK = 399268537       #/* use 1043616065 for the "minimal standard" */ 
MODULUS = 2147483647    #/* DON'T CHANGE THIS VALUE                   */
MULTIPLIER = 48271      #/* use 16807 for the "minimal standard"      */
DEFAULT = 123456789
seed = int(DEFAULT)


def random(): 
  #/* ---------------------------------------------------------------------
  #* Random is a Lehmer generator that returns a pseudo-random real number
  #* uniformly distributed between 0.0 and 1.0.  The period is (m - 1)
  #* where m = 2,147,483,647 amd the smallest and largest possible values
  #* are (1 / m) and 1 - (1 / m) respectively.
  #* ---------------------------------------------------------------------
  #*/
  global seed

  Q = int(MODULUS / MULTIPLIER)
  R = int(MODULUS % MULTIPLIER)

  t = int(MULTIPLIER * (seed % Q) - R * int(seed / Q))
  if (t > 0):
    seed = int(t)
  else:
    seed = int(t + MODULUS)

  return float(seed / MODULUS)

def putSeed(x):
  # /* -------------------------------------------------------------------
  #  * Use this (optional) procedure to initialize or reset the state of
  #  * the random number generator according to the following conventions:
  #  *    if x > 0 then x is the initial seed (unless too large)
  #  *    if x < 0 then the initial seed is obtained from the system clock
  #  *    if x = 0 then the initial seed is to be supplied interactively
  #  * --------------------------------------------------------------------
  #  */
  global seed 

  ok = False

  if (x > 0):
    x = x % MODULUS  
                            # correct if x is too large  
  if (x < 0): 
    x = time()
    x = x % MODULUS
  
  if (x == 0):
    while (ok == False): 
      line = input("\nEnter a positive integer seed (9 digits or less) >> ")
      x = int(line)
      ok = (0 < x) and (x < MODULUS)
      if (ok == False):
        print("\nInput out of range ... try again\n")
    
    
  seed = int(x)


def getSeed():
  # /* --------------------------------------------------------------------
  #  * Use this (optional) procedure to get the current state of the random
  #  * number generator.
  #  * --------------------------------------------------------------------
  #  */
  return seed


  
def testRandom():
  # /* -------------------------------------------------------------------
  #  * Use this (optional) procedure to test for a correct implementation.
  #  * -------------------------------------------------------------------
  #  */

  putSeed(1);                                 #/* set initial state to 1 */
  for i in range(0,10000):
    u = random()

  x = getSeed()
  if (CHECK == x):
    print("\n The implementation of Random is correct")
  else:
    print("\n ERROR - the implementation of Random is not correct")

  
