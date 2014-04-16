# -------------------------------------------------------------------------
# * This program is a next-event simulation of a single-server FIFO service
# * node using Exponentially distributed interarrival times and Uniformly
# * distributed service times (i.e., a M/U/1 queue). The service node is
# * assumed to be initially idle, no arrivals are permitted after the
# * terminal time STOP, and the service node is then purged by processing any
# * remaining jobs in the service node.
# *
# * Name : ssq3.c (Single Server Queue, version 3)
# * Author : Steve Park & Dave Geyer
# * Language : ANSI C
# * Latest Revision : 10-19-99
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
# * -------------------------------------------------------------------------
# */

from rngs import random, plantSeeds, selectStream
from math import log

START = 0.0 # initial time */
STOP = 20000.0 # terminal (close the door) time */
INFINITY = (100.0 * STOP) # must be much larger than STOP */


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

##################################################
plantSeeds(123456789)
selectStream(0)

for i in range(0,1000):
    print("{0:f}".format(Exponential(1)))


# C output (last 10 rows):
# 1.276245
# 0.466973
# 0.053791
# 2.774928
# 0.116793
# 2.878659
# 1.149758
# 2.682214
# 1.230311
# 0.141221
# 0.553774