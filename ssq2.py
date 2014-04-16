
# ------------------------------------------------------------------------- 
# * This program - an extension of program ssq1.c - simulates a single-server 
# * FIFO service node using Exponentially distributed interarrival times and 
# * Uniformly distributed service times (i.e. a M/U/1 queue). 
# *
# * Name              : ssq2.c  (Single Server Queue, version 2)
# * Author            : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 9-11-98
#   Translated by   : Philip Steele 
#   Language        : Python 3.3
#   Latest Revision : 3/26/14
# * ------------------------------------------------------------------------- 
# */

from rng import putSeed, random
from math import log

LAST = 10000                   # number of jobs processed */ 
START = 0.0                      # initial time             */ 
arrivalTemp = START #global for getArrival 


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
# ------------------------------
# * generate the next arrival time
# * ------------------------------
# */     
  global arrivalTemp                                       

  arrivalTemp += Exponential(2.0)
  return (arrivalTemp)



def GetService():
# ------------------------------
# * generate the next service time
# * ------------------------------
# */ 
  return (Uniform(1.0, 2.0))


class sumOf:
  delay = 0.0  #delay times
  wait = 0.0 #wait times
  service = 0.0 #service times
  interarrival = -1.0 #interarrival times

#################################Main Program############################

index = 0                        # job index            */
arrival = START                    # arrival time         */
delay = -1                               # delay in queue       */
service = -1                             # service time         */
wait = -1                                 # delay + service      */
departure = START                    # departure time       */
sum = sumOf()

putSeed(123456789)

while (index < LAST):
  index += 1
  arrival      = GetArrival()
  if (arrival < departure):
    delay      = departure - arrival         # delay in queue    */
  else:
    delay      = 0.0                         # no delay          */
  service      = GetService()
  wait         = delay + service
  departure    = arrival + wait              # time of departure */
  sum.delay   += delay
  sum.wait    += wait
  sum.service += service
#EndWhile 
sum.interarrival = arrival - START

print("\nfor {0} jobs".format(index))
print("   average interarrival time = {0:6.2f}".format(sum.interarrival / index))
print("   average wait ............ = {0:6.2f}".format(sum.wait / index))
print("   average delay ........... = {0:6.2f}".format(sum.delay / index))
print("   average service time .... = {0:6.2f}".format(sum.service / index))
print("   average # in the node ... = {0:6.2f}".format(sum.wait / departure))
print("   average # in the queue .. = {0:6.2f}".format(sum.delay / departure))
print("   utilization ............. = {0:6.2f}".format(sum.service / departure))

#C output:
# for 10000 jobs
#    average interarrival time =   2.02
#    average wait ............ =   3.86
#    average delay ........... =   2.36
#    average service time .... =   1.50
#    average # in the node ... =   1.91
#    average # in the queue .. =   1.17
#    utilization ............. =   0.74

