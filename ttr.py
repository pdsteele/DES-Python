# ------------------------------------------------------------------------- 
# * This program is a next-event simulation of a multi-user time-sharing
# * system.  All users begin with the thinking task and the simulation ends 
# * when the simulation clock time meets or exceeds the terminal time STOP.
# * 
# * Name              : ttr.c (Think-Type-Receive)
# * Author            : Larry Leemis 
# * Language          : ANSI C 
# * Latest Revision   : 10-12-04 
#  # Translated by    : Philip Steele 
#  # Language         : Python 3.3
#  # Latest Revision  : 3/26/14
# * ------------------------------------------------------------------------- 
# */

from rngs import selectStream, plantSeeds, random
from math import exp, log, pow, sqrt

START =  0.0                     # initial simulation clock time  */
STOP =   100.0                   # terminal time                  */
N    =    5                      # number of servers              */

def Equilikely(a,b):
# ===================================================================
# * Returns an equilikely distributed integer between a and b inclusive. 
# * NOTE: use a < b
# * ===================================================================
# */
  return (a + int((b - a + 1) * random()))


def Uniform(a,b):
# =========================================================== 
# * Returns a uniformly distributed real number between a and b. 
# * NOTE: use a < b
# * ===========================================================
# */
  return (a + (b - a) * random())

   

def GetThinkTime():
# ----------------------------
# * generate the next think time 
# * ----------------------------
# */     
  selectStream(0)
  return (Uniform(0.0, 10.0))


   
def GetKeystrokeTime():
# -------------------------------
# * generate the next keystroke time 
# * -------------------------------
# */     
  selectStream(1)
  return (Uniform(0.15, 0.35))


   
def GetNumKeystrokes():
# ---------------------------------
# * generate the number of keystrokes 
# * ---------------------------------
# */   
  selectStream(2)
  return (Equilikely(5, 15))

   
def GetNumCharacters():
# ---------------------------------
# * generate the number of characters 
# * ---------------------------------
# */   
  selectStream(3)
  return (Equilikely(50, 300))

class events:
  time = None  #Event time
  type = None  #Event Type
  info = None  #Ancillary info
#############################################Main Program##########################
# i                          # loop parameter                         */
# j                          # index for the next event               */
nevents = 0                  # number of events during the simulation */
nsearches = 0                # number of event list searches          */
tnow = START                 # simulation clock                       */
# temp                       # used to find time of next event        */
ReceiveRate = 1.0 / 120.0    # time to transmit a character           */
event = [events() for i in range(0,N)]

plantSeeds(0)
tnow = START
for i in range(0,N): 
  event[i].time = GetThinkTime()
  event[i].type = 1
  event[i].info = 0


while (tnow < STOP): 
  nevents+= 1
  temp = 100.0 * STOP
  for i in range(0,N): 
    nsearches+= 1
    if (event[i].time <= temp):
      temp = event[i].time
      j = i
    #EndIf
  #EndFor
  tnow = event[j].time   
  if (event[j].type == 1):          # complete thinking event  */
    event[j].time = tnow + GetKeystrokeTime()
    event[j].type = 2
    event[j].info = GetNumKeystrokes()
  #EndIf
  elif (event[j].type == 2):        # complete keystroke event */
    event[j].info -= 1 
    if (event[j].info > 0):
      event[j].time = tnow + GetKeystrokeTime()
    else:                            # last keystroke           */
      event[j].time = tnow + ReceiveRate 
      event[j].type = 3
      event[j].info = GetNumCharacters()
  #EndElif
  elif (event[j].type == 3):        # complete character recpt */
    event[j].info -= 1 
    if (event[j].info > 0):
      event[j].time = tnow + ReceiveRate 
    else:                            # last character           */
      event[j].time = tnow + GetThinkTime() 
      event[j].type = 1
      event[j].info = 0
  #EndElif
  else:
    print("\nerror: event type must be 1, 2, or 3")  
 

print("\nsimulation end time .... = {0:6.2f}".format(tnow))
print("\nfinal status of the event list:")  
for i in range(0,N):
  print("{0:8d} {1:14.3f} {2:8d} {3:8d}".format(i, event[i].time, event[i].type, event[i].info))

print("\nnumber of events ....... = {0:1d}".format(nevents))
print("\nnumber of searches ..... = {0:1d}".format(nsearches))




# C output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# simulation end time .... = 100.01

# final status of the event list:
#        0        100.010        2        6
#        1        100.065        2        1
#        2        100.166        2       12
#        3        100.098        1        0
#        4        100.015        3      237

# number of events ....... = 10882

# number of searches ..... = 54410