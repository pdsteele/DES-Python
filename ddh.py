# # ------------------------------------------------------------------------- 
#  * This program illustrates a linked-list algorithm for tallying a 
#  * discrete-data histogram for data read from standard input (stdin).   
#  * Like program uvs, a compiled version of this program supports file 
#  * redirection. 
#  * 
#  * NOTE: if the data is not discrete, i.e., virtually all inputs are likely 
#  * to be unique, and if the number of inputs is large (say 10,000 or more)
#  * then this program will execute for a LOOOONG time!
#  *
#  * Name            : ddh.c  (Discrete Data Histogram)
#  * Authors         : Steve Park & Dave Geyer
#  * Language        : ANSI C
#  * Latest Revision : 10-05-98
#  # Translated by     : Philip Steele 
#  # Language          : Python 3.3
#  # Latest Revision   : 3/26/14
#  * ------------------------------------------------------------------------- 
#  */

from math import sqrt
import sys

class node:
  def __init__(self,value):
    self.value = value
    self.count = 1
    self.next = None

  def insert(self,value):
    #Add 'data' to the list
    
    found = False
    lastNode = self
    nextNode = self.next
    #find end or node with same value
    while(found == False):
      if nextNode == None:
        newNode = node(value)
        lastNode.next = newNode
        found = True
      elif (nextNode.value == value):
        nextNode.count += 1
        found = True
      else:
        lastNode = nextNode
        nextNode = nextNode.next #go to next node

def sort(head):
  #sort the list with good ol' fashioned selection sort
  p = head
  while(p != None):
    q = p
    min = q.value
    while(q != None):         # find the smallest unsorted value */
      if(q.value < min):
        min = q.value
      q = q.next

    q = p
    while(q.value != min):  # find the node containing 'min' */
      q = q.next
    swap(p,q)               #Swap the min to p's position 
    p = p.next


def swap(node1, node2):
  #swap the contents of two nodes
  temp1 = node1.value
  temp2 = node1.count
  node1.value = node2.value
  node1.count = node2.count
  node2.value = temp1
  node2.count = temp2 


def traverse(head):
  #traverse list to computer histogram statistics and print 
  # the histogram
                                    
  # pointer  p
  index  = 0
  sum    = 0.0
  sumsqr = 0.0

  p = head
  while (p != None):                 # traverse the list               */ 
    index += p.count                # to accumulate 'sum' and 'index' */
    sum   += p.value * p.count
    p      = p.next
  #EndWhile
  mean = sum / index

  p = head                            # traverse the list      */
  while (p != None):                  # to accumulate 'sumsqr' */
    diff    = p.value - mean
    sumsqr += diff * diff * p.count
    p       = p.next
  
  stdev = sqrt(sumsqr / index)
  print("     value      count   proportion\n")
  p = head                            # traverse the list      */
  while (p != None):                  # to print the histogram */
    print("{0:10.2f} {1:10d} {2:12.3f}".format(p.value, p.count, float(p.count / index)))
    p = p.next
  
  print("\nsample size ........... = {0:7d}".format(index))
  print("mean .................. = {0:7.3f}".format(mean))
  print("standard deviation .... = {0:7.3f}".format(stdev))






######################################MAIN Program############################
data = sys.stdin.readline()
if (data):
  head = node(float(data))
else:
  head = None

data = sys.stdin.readline()
while (data):
  head.insert(float(data))
  data = sys.stdin.readline()

if (head != None):
  sort(head)
  traverse(head)



# C output:
#      value      count   proportion

#       0.00         11        0.011
#       1.00        162        0.162
#       2.00        262        0.262
#       3.00        245        0.245
#       4.00        147        0.147
#       5.00         76        0.076
#       6.00         49        0.049
#       7.00         29        0.029
#       8.00         15        0.015
#       9.00          2        0.002
#      10.00          1        0.001
#      11.00          1        0.001

# sample size ........... =    1000
# mean .................. =   3.045
# standard deviation .... =   1.710