# # -----------------------------------------------------------------------
#  * This program - an extension of program ssq2 - simulates a single-server 
#  * machine shop using Exponentially distributed failure times, Uniformly 
#  * distributed service times, and a FIFO service queue.  
#  *
#  * Name            : ssms.c  (Single Server Machine Shop)
#  * Authors         : Steve Park & Dave Geyer
#  * Language        : ANSI C
#  * Latest Revision : 9-28-98 
#  * -----------------------------------------------------------------------
#  */
from rngs import random, plantSeeds, selectStream
from math import log
 
#include <stdio.h>
#include <math.h>                                             
#include "rngs.h"

LAST = 100000                  # number of machine failures */
START = 0.0                     # initial time               */
M = 60                      # number of machines         */


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


def GetFailure():
# # ------------------------------------------------ 
#  * generate the operational time until next failure 
#  * ------------------------------------------------
#  */
  selectStream(0)
  return (Exponential(100.0))



def NextFailure(failure,m):
# # -----------------------------------------------------------------
#  * return the next failure time, and the index of the failed machine
#  * -----------------------------------------------------------------
#  */
# failure and m are lists

  i = 0
  t = float(failure[0])

  m[0] = i
  for i in range(1,M):
    if (failure[i] < t): 
      t = failure[i]
      m[0] = i
  #EndFor

  return (t)


def GetService():
# # ------------------------------
#  * generate the next service time
#  * ------------------------------
#  */ 
  selectStream(1)
  return (Uniform(1.0, 2.0))

class sumOf:
  wait = 0.0  #wait times
  delay = 0.0 #delay times
  service = 0.0 #service times
  interarrival = -1.0 #interarrival times

##############################Main Program################################

index = 0                    # job (machine failure) index */
arrival   = START                # time of arrival (failure)   */
delay = -1.0                           # delay in repair  queue      */
service = -1.0                         # service (repair) time       */
wait = -1.0                             # delay + service             */
departure = START                # time of service completion  */
m = 0                                # machine index 0,1,...(M-1)  */
failure = []                       # list of next failure times  */ 
sum = sumOf()

plantSeeds(123456789)

for m in range(0,M):                 # initial failures */
  failure.append(START + GetFailure())

m = [m] #convert to list to become mutable when passing to NextFailure

while (index < LAST):
  index += 1
  arrival      = NextFailure(failure,m)

  if (arrival < departure):
    delay      = departure - arrival  
  else:
    delay      = 0.0 

  service      = GetService()
  wait         = delay + service
  departure    = arrival + wait           # completion of service  */
  failure[m[0]]   = departure + GetFailure() # next failure, machine m */
  sum.wait    += wait
  sum.delay   += delay
  sum.service += service
#EndWhile 

sum.interarrival = arrival - START

print("\nfor a pool of {0:1d} machines and {1:1d} simulated failures\n".format(M,index)) 
print("average interarrival time .. = {0:6.2f}".format(sum.interarrival / index))
print("average wait ............... = {0:6.2f}".format(sum.wait / index))
print("average delay .............. = {0:6.2f}".format(sum.delay / index))
print("average service time ....... = {0:6.2f}".format(sum.service / index))
print("average # in the node ...... = {0:6.2f}".format(sum.wait / departure))
print("average # in the queue ..... = {0:6.2f}".format(sum.delay / departure))
print("utilization ................ = {0:6.2f}".format(sum.service / departure))

#C output:
# for a pool of 60 machines and 100000 simulated failures

# average interarrival time .. =   1.75
# average wait ............... =   5.09
# average delay .............. =   3.59
# average service time ....... =   1.50
# average # in the node ...... =   2.90
# average # in the queue ..... =   2.05
# utilization ................ =   0.86