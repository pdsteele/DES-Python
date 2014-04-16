# # ------------------------------------------------------------------------- 
#  * This program is a next-event simulation of a single-server FIFO service
#  * node using Exponentially distributed interarrival times and Uniformly 
#  * distributed service times (i.e., a M/U/1 queue).  The service node is 
#  * assumed to be initially idle, no arrivals are permitted after the 
#  * terminal time STOP, and the service node is then purged by processing any 
#  * remaining jobs in the service node.
#  *
#  * Name            : ssq3.c  (Single Server Queue, version 3)
#  * Author          : Steve Park & Dave Geyer
#  * Language        : ANSI C
#  * Latest Revision : 10-19-98
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
#  * ------------------------------------------------------------------------- 
#  */

from math import log
from rngs import plantSeeds, random, selectStream # the multi-stream generator - ENSURE rngs.py in same folder */

START =        0.0              # initial time                   */
STOP  =    20000.0              # terminal (close the door) time */
INFINITY =  (100.0 * STOP)      # must be much larger than STOP  */
arrivalTemp = START             # global temp var for getArrival function


def Min(a,c):
# ------------------------------
# * return the smaller of a, b
# * ------------------------------
# */
  if (a < c):
    return (a)
  else:
    return (c)

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




def GetArrival():
# ---------------------------------------------
# * generate the next arrival time, with rate 1/2
# * ---------------------------------------------
# */ 
  global arrivalTemp

  selectStream(0) 
  arrivalTemp += Exponential(2.0)
  return (arrivalTemp)



def GetService():
# --------------------------------------------
# * generate the next service time with rate 2/3
# * --------------------------------------------
# */ 
  selectStream(1)
  return (Uniform(1.0, 2.0))

class track:
  node = 0.0                   # time integrated number in the node  */
  queue = 0.0                  # time integrated number in the queue */
  service = 0.0                # time integrated number in service   */

class time:
  arrival = -1                # next arrival time                   */
  completion = -1             # next completion time                */
  current  = -1               # current time                        */
  next = -1                   # next (most imminent) event time     */
  last = -1                   # last arrival time                   */

##########################Main Program##################################

index  = 0                  # used to count departed jobs         */
number = 0                  # number in the node                  */
area = track()
t = time()

plantSeeds(123456789)

t.current    = START           # set the clock                         */
t.arrival    = GetArrival()    # schedule the first arrival            */
t.completion = INFINITY        # the first event can't be a completion */

while (t.arrival < STOP) or (number > 0):
  t.next          = Min(t.arrival, t.completion)  # next event time   */
  if (number > 0):                               # update integrals  */
    area.node    += (t.next - t.current) * number
    area.queue   += (t.next - t.current) * (number - 1)
    area.service += (t.next - t.current)
  #EndIf

  t.current       = t.next                    # advance the clock */

  if (t.current == t.arrival):               # process an arrival */
    number += 1
    t.arrival     = GetArrival()
    if (t.arrival > STOP):
      t.last      = t.current
      t.arrival   = INFINITY

    if (number == 1):
      t.completion = t.current + GetService()
  #EndOuterIf
  else:                                        # process a completion */
    index += 1
    number -= 1
    if (number > 0):
      t.completion = t.current + GetService()
    else:
      t.completion = INFINITY
  
#EndWhile 

print("\nfor {0} jobs".format(index))
print("   average interarrival time = {0:6.2f}".format(t.last / index))
print("   average wait ............ = {0:6.2f}".format(area.node / index))
print("   average delay ........... = {0:6.2f}".format(area.queue / index))
print("   average service time .... = {0:6.2f}".format(area.service / index))
print("   average # in the node ... = {0:6.2f}".format(area.node / t.current))
print("   average # in the queue .. = {0:6.2f}".format(area.queue / t.current))
print("   utilization ............. = {0:6.2f}".format(area.service / t.current))

#C output:
# for 10025 jobs
#    average interarrival time =   1.99
#    average wait ............ =   3.92
#    average delay ........... =   2.41
#    average service time .... =   1.50
#    average # in the node ... =   1.96
#    average # in the queue .. =   1.21
#    utilization ............. =   0.75