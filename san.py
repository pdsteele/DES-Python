# *  --------------------------------------------------------------------------  *
#  * A Monte Carlo simulation of a stochastic activity network.                  *
#  *                                                                             *
#  * Name              : san.c                                                   *
#  * Author            : Jeff Mallozzi, Kerry Connell, Larry Leemis, Matt Duggan *
#  * Language          : ANSI C                                                  *
#  * Latest Revision   : 6-16-04                                                 *
#  # Translated by   : Philip Steele 
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14                                    *
#  ----------------------------------------------------------------------------- */


from math import sqrt, log, exp
from rngs import random, putSeed

MAXEDGE = 50
MAXNODE = 50
MAXPATHS = 50
N = 10000                           # number of replications */

M = [[None for i in range(0,MAXEDGE)] for i in range(0,MAXNODE)]
Paths = [[None for i in range(0,MAXEDGE)] for i in range(0,MAXPATHS)]
UpperLimit = [None for i in range(0,MAXEDGE)]
p = [None for i in range(0,MAXEDGE)]
paths = None
nodes = None
edges = None

def Uniform(a,b):  
#  ---------------------------------------------
# * generate a Uniform random variate, use a < b 
# *--------------------------------------------- 
# */
  return (a + (b - a) * random())  

# ========================== */
def GetActivityDurations():
# ========================== */
  for i in range(1,edges+1):
    p[i] = Uniform(0.0, UpperLimit[i])

  return()

# ================ */
def PrintPaths():
# ================ */
  print("")
  for i in range(1,paths+1):
    print("Path {0:1d}: ".format(i), end='')
    j = 1
    while(Paths[i][j] != 0):
      j += 1
    #EndWhile
    j -= 1
    while(j > 0):
      print("-{0:1d}-".format(Paths[i][j]), end='')
      j -= 1
    #EndWhile
    print("")
  #EndFor
  return()


# =============================== */
def TimeToComplete(node):
# =============================== */
  l = 0
  tmax   = 0.0
  t  = 0.0
  k = 1

  while (l < M[node][0]):
    if (M[node][k] == -1):
      t = TimeToComplete(M[0][k]) + p[k]
      if (t >= tmax):
        tmax = t
      #EndInnerIf
      l += 1
    #EndOuterIf
    k += 1
  #EndWhile
  return(tmax)

# ============================================= */
def GetPaths(node,step,path):
# ============================================= */

  i = 1
  found    = 0
  numpaths = 0
  total    = 0
  
  while(found < M[node][0]):
    if(M[node][i] == -1):
      numpaths = GetPaths(M[0][i], step + 1, path + total)
      for j in range(0,numpaths):
        Paths[path + j + total][step] = i
      #EndFor
      total += numpaths
      found += 1
    #EndIf
    i += 1
  #EndWhile

  if(total == 0):
    Paths[path][step] = 0
    total = 1
  

  return(total)


# ============================================= */
def EstimatePathProb():
# ============================================= */
  PathProb = [0 for i in range(0,MAXPATHS)] 
  pathtime = 0.0
  maxtime = 0.0
  
  for i in range(0,N):
    GetActivityDurations()

    for j in range(1,paths+1):
      k = 1
      while(Paths[j][k] != 0):
        pathtime += p[Paths[j][k]]
        k += 1
      #EndWhile
      if(pathtime > maxtime): 
        maxtime = pathtime
        maxpath = j
      #EndIf
      pathtime = 0.0
    #EndInnerFor
    PathProb[maxpath] += 1
    
    maxpath = 0
    maxtime = 0.0
  #EndFor

  print("\nCritical path probabilities:")
  for i in range(1,paths+1):
    print(" -  {0:2d}  - ".format(i), end='')
  print("")
  for i in range(1,paths+1):
    print(" {0:1.6f} ".format(float(PathProb[i])/N),end='')
  print("")

  return()

# =================== */
def DefineNetwork():
# =================== */
  global paths
  global edges
  global nodes

  edges = 9
  nodes = 6

  for j in range(0,nodes+1):
    for k in range(0,edges+1):
      M[j][k] = 0
    
  
  M[1][1] = 1
  M[2][1] = -1
  M[1][2] = 1
  M[3][2] = -1
  M[1][3] = 1
  M[4][3] = -1
  M[2][4] = 1
  M[3][4] = -1
  M[2][5] = 1
  M[5][5] = -1
  M[3][6] = 1
  M[4][6] = -1
  M[3][7] = 1
  M[6][7] = -1
  M[4][8] = 1
  M[6][8] = -1
  M[5][9] = 1
  M[6][9] = -1

  for j in range(1,nodes+1):
    for k in range(1,edges+1):
      if(M[j][k] == -1):
        M[j][0] += 1
      elif(M[j][k] == 1):
        M[0][k] = j

  UpperLimit[1] = 3.0
  UpperLimit[2] = 6.0
  UpperLimit[3] = 13.0
  UpperLimit[4] = 9.0
  UpperLimit[5] = 3.0
  UpperLimit[6] = 9.0
  UpperLimit[7] = 7.0
  UpperLimit[8] = 6.0
  UpperLimit[9] = 3.0

  paths = GetPaths(nodes, 1, 1)

  print("Network read in:")
  print("{0:1d} edges.".format(edges))
  print("{0:1d} nodes.".format(nodes))
  print("{0:1d} paths.".format(paths))

  return()


# ============================ */
def EstimateCompletionTime():
# ============================ */
  
  sumtime = 0.0
  
  node = nodes 

  for i in range(0,N):
    GetActivityDurations()
    time = TimeToComplete(node)
    sumtime += time 
  

  print("\nFor {0:1d} replications,".format(N))
  print("the estimated average time to complete the network is:") 
  print("{0:11.5f}".format(sumtime / float(N)))

  return()

####################################Main program#########################
DefineNetwork()
PrintPaths()
putSeed(0)
EstimateCompletionTime()
putSeed(0)
EstimatePathProb()


# C output:
# Network read in:
# 9 edges.
# 6 nodes.
# 6 paths.

# Path 1: -2--7-
# Path 2: -1--4--7-
# Path 3: -3--8-
# Path 4: -2--6--8-
# Path 5: -1--4--6--8-
# Path 6: -1--5--9-

# Enter a positive integer seed (9 digits or less) >> 123456789

# For 10000 replications,
# the estimated average time to complete the network is:
#    14.58729

# Enter a positive integer seed (9 digits or less) >> 123

# Critical path probabilities:
#  -   1  -  -   2  -  -   3  -  -   4  -  -   5  -  -   6  -
#  0.017500  0.092300  0.190900  0.116300  0.582000  0.001000
