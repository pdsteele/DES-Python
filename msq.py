# ------------------------------------------------------------------------- 
# * This program is a next-event simulation of a multi-server, single-queue 
# * service node.  The service node is assumed to be initially idle, no 
# * arrivals are permitted after the terminal time STOP and the node is then 
# * purged by processing any remaining jobs. 
# * 
# * Name              : msq.c (Multi-Server Queue)
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 10-19-98 
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
# * ------------------------------------------------------------------------- 
# */

from rngs import plantSeeds, random, selectStream
from math import log

START =   0.0                    # initial (open the door)        */
STOP  =   20000.0                # terminal (close the door) time */
SERVERS = 4                      # number of servers              */
arrivalTemp = START

# typedef struct {                        # the next-event list    */
#   double t                             #   next event time      */
#   int    x                             #   event status, 0 or 1 */
# } event_list[SERVERS + 1]              

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
# * generate the next service time with rate 1/6
# * --------------------------------------------
# */ 
  selectStream(1)
  return (Uniform(2.0, 10.0))


def NextEvent(events):
# ---------------------------------------
# * return the index of the next event type
# * ---------------------------------------
# */

  i = 0

  while (events[i].x == 0):       # find the index of the first 'active' */
    i += 1                        # element in the event list            */ 
  #EndWhile
  e = i

  while (i < SERVERS):         # now, check the others to find which  */
    i += 1                        # event type is most imminent          */
    if ((events[i].x == 1) and (events[i].t < events[e].t)):
      e = i
  #EndWhile
  
  return (e)

def FindOne(events):
# -----------------------------------------------------
# * return the index of the available server idle longest
# * -----------------------------------------------------
# */
  i = 1

  while (events[i].x == 1):       # find the index of the first available */
    i += 1                        # (idle) server                         */
  #EndWhile
  s = i
  while (i < SERVERS):         # now, check the others to find which   */ 
    i += 1                        # has been idle longest                 */
    if ((events[i].x == 0) and (events[i].t < events[s].t)):
      s = i
  #EndWhile 

  return (s)

class event:
  t = None  #next event time
  x = None  #event status, 0 or 1

class time:
  current = None          # current time                       */
  next = None             # next (most imminent) event time    */

class accumSum:
                          # accumulated sums of                */
  service = None          #   service times                    */
  served = None           #   number served                    */

############################Main Program###################################

t = time()
events = [event() for i in range(SERVERS + 1)]
number = 0             # number in the node                 */
#e                      # next event index                   */
#s                      # server index                       */
index  = 0             # used to count processed jobs       */
area   = 0.0           # time integrated number in the node */
sum=[accumSum() for i in range(0,SERVERS + 1)]

plantSeeds(0)
t.current    = START
events[0].t   = GetArrival()
events[0].x   = 1
for s in range(1,SERVERS+1):
  events[s].t     = START          # this value is arbitrary because */
  events[s].x     = 0              # all servers are initially idle  */
  sum[s].service = 0.0
  sum[s].served  = 0


while ((events[0].x != 0) or (number != 0)):
  e         = NextEvent(events)                  # next event index */
  t.next    = events[e].t                        # next event time  */
  area     += (t.next - t.current) * number     # update integral  */
  t.current = t.next                            # advance the clock*/

  if (e == 0):                                  # process an arrival*/
    number += 1
    events[0].t        = GetArrival()
    if (events[0].t > STOP):
      events[0].x      = 0
    #EndIf
    if (number <= SERVERS):
      service  = GetService()
      s               = FindOne(events)
      sum[s].service += service
      sum[s].served += 1
      events[s].t      = t.current + service
      events[s].x      = 1
    #EndIf
  #EndIf
  else:                                          # process a departure */
    index += 1                                     # from server s       */  
    number -= 1
    s = e                       
    if (number >= SERVERS): 
      service   = GetService()
      sum[s].service += service
      sum[s].served += 1
      events[s].t      = t.current + service
    else:
      events[s].x      = 0
  #EndElse
#EndWhile

print("\nfor {0:1d} jobs the service node statistics are:\n".format(index))
print("  avg interarrivals .. = {0:6.2f}".format(events[0].t / index))
print("  avg wait ........... = {0:6.2f}".format(area / index))
print("  avg # in node ...... = {0:6.2f}".format(area / t.current))

for s in range(1,SERVERS+1):            # adjust area to calculate */ 
     area -= sum[s].service              # averages for the queue   */    

print("  avg delay .......... = {0:6.2f}".format(area / index))
print("  avg # in queue ..... = {0:6.2f}".format(area / t.current))
print("\nthe server statistics are:\n")
print("    server     utilization     avg service        share\n")
for s in range(1,SERVERS+1):
  print("{0:8d} {1:14.3f} {2:15.2f} {3:15.3f}".format(s, sum[s].service / t.current, sum[s].service / sum[s].served,float(sum[s].served) / index))

# C output:
# for 10025 jobs the service node statistics are:

#   avg interarrivals .. =   2.00
#   avg wait ........... =   7.96
#   avg # in node ...... =   3.99
#   avg delay .......... =   1.94
#   avg # in queue ..... =   0.97

# the server statistics are:

#     server     utilization     avg service        share
#        1          0.754            6.04           0.249
#        2          0.755            5.97           0.252
#        3          0.754            6.05           0.249
#        4          0.757            6.05           0.250

