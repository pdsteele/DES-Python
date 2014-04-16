# -------------------------------------------------------------------------  
# * This program is a next-event simulation of a simple inventory system with 
# * a Poisson demand process, backlogging, and a Uniform(0,1) delivery lag. 
# *
# * Name              : sis3.c  (Simple Inventory System, version 3) 
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 10-19-98 
#   Translated by     : Philip Steele 
#   Language          : Python 3.3
#   Latest Revision   : 3/26/14
# * ------------------------------------------------------------------------- 
# */
from rngs import random, plantSeeds, selectStream
from math import log

MINIMUM =   20             # 's' inventory policy parameter >= 0 */
MAXIMUM =   80             # 'S' inventory policy parameter > s  */
START =     0.0
STOP =      100.0
INFINITY =   (100.0 * STOP)

tempTime = START #global to act as static var for GetDemand()
 

def Exponential(m):
# ---------------------------------------------------
# * generate an Exponential random variate, use m > 0.0 
# * ---------------------------------------------------
# */
  return (-m * log(1.0 - random()))



def Uniform(a,b):  
# --------------------------------------------
# * generate a Uniform random variate, use a < b 
# * --------------------------------------------
# */
  return (a + (b - a) * random())  


def GetDemand():
# --------------------------------------------------------------
# * generate the next demand instance (time) with rate 30 per time 
# * interval and exactly one unit of demand per demand instance 
# * --------------------------------------------------------------
# */      
  global tempTime

  selectStream(0)
  tempTime += Exponential(1.0 / 30.0)
  return (tempTime)


def GetLag():
# ------------------------------
# * generate a delivery lag (time) 
# * ------------------------------
# */                                        
  selectStream(1)
  return (Uniform(0.0, 1.0))


def Min(a,b,c):    
# ----------------------------------------
# * return the smallest of a, b, c
# * ----------------------------------------
# */
  t = a

  if (b < t):
    t = b
  if (c < t):
    t = c
  return (t)


class sumOf:
  setup = 0.0     #setup instances
  holding = 0.0   #inventory held (+)
  shortage = 0.0  #inventory held (-)
  order = 0.0     #orders
  demand = 0.0    #demands
  lag = 0.0      #lags

class time:
  demand  = 0    # next demand time                */
  arrive  = 0         # next order arrival time init with no order  */
  current = 0            # current time                    */
  review  = 0     # next inventory review time      */
  next = 0  # next (most imminent) event time */

############################Main Program##########################


inventory = MAXIMUM            # current inventory level */
order     = 0                  # current order level     */
t = time()
sum = sumOf()

plantSeeds(0)

t.current = START
t.demand  = GetDemand()              #/* schedule the first demand */
t.review  = t.current + 1.0          #/* schedule the first review */
t.arrive  = INFINITY           #/* no order arrival pending  */

while (t.current < STOP):
  t.next          = Min(t.demand, t.review, t.arrive)

  if (inventory > 0):
    sum.holding  += (t.next - t.current) * inventory
  else:
    sum.shortage -= (t.next - t.current) * inventory
  t.current       = t.next

  if (t.current == t.demand):        # process an inventory demand */
    sum.demand += 1
    inventory -= 1
    t.demand = GetDemand()

  elif (t.current == t.review):   # process inventory review */
    if (inventory < MINIMUM):
      order      = int(MAXIMUM - inventory)
      lag        = GetLag()
      sum.setup += 1
      sum.order += order
      sum.lag   += lag
      t.arrive   = t.current + lag
    #EndInnerIf
    t.review  = t.current + 1.0

  else:                           # process an inventory order arrival*/
    inventory += int(order)
    order      = 0
    t.arrive   = INFINITY
#EndWhile

if (inventory < MAXIMUM):          # adjust the final inventory level */
  order      = MAXIMUM - inventory
  sum.setup += 1
  sum.order += order
  inventory += order


print("\nfor {0:1d} time intervals with an average demand of {1:6.2f}".format(int(STOP),(sum.demand / STOP))) 
if (sum.setup > 0.0):
  print("an average lag of {0:4.2f}".format(sum.lag / sum.setup))
print(" and policy parameters (s, S) = ({0},{1})\n".format(MINIMUM, MAXIMUM))
print("   average order ............ = {0:6.2f}".format(sum.order / STOP))
print("   setup frequency .......... = {0:6.2f}".format(sum.setup / STOP))
print("   average holding level .... = {0:6.2f}".format(sum.holding / STOP))
print("   average shortage level ... = {0:6.2f}".format(sum.shortage / STOP))

#C output:

# Enter a positive integer seed (9 digits or less) >> 123456789

# for 100 time intervals with an average demand of  30.03
# an average lag of 0.49 and policy parameters (s, S) = (20, 80)

#    average order ............ =  30.03
#    setup frequency .......... =   0.40
#    average holding level .... =  28.59
#    average shortage level ... =   1.68
