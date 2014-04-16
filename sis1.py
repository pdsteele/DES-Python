
# -------------------------------------------------------------------------
#  * This program simulates a simple (s,S) inventory system using demand read  
#  * from a text file.  Backlogging is permitted and there is no delivery lag.
#  * The output statistics are the average demand and order per time interval
#  * (they should be equal), the relative frequency of setup and the time
#  * averaged held (+) and short (-) inventory levels.
#  *
#  * NOTE: use 0 <= MINIMUM < MAXIMUM, i.e., 0 <= s < S.
#  *
#  * Name              : sis1.c  (Simple Inventory System, version 1)
#  * Authors           : Steve Park & Dave Geyer 
#  * Language          : ANSI C 
#  * Latest Revision   : 8-20-97 
#  * Compile with      : gcc sis1.c
#    Translated by   : Philip Steele 
#    Language        : Python 3.3
#    Latest Revision : 3/26/14
#  * ------------------------------------------------------------------------- 
#  */                     

FILENAME = "sis1.dat"            # input data file                */
MINIMUM = 20                    # 's' inventory policy parameter */
MAXIMUM = 80                    # 'S' inventory policy parameter */


class sumOf:
  setup = 0.0     #setup instances
  holding = 0.0   #inventory held (+)
  shortage = 0.0  #inventory held (-)
  order = 0.0     #orders
  demand = 0.0    #demands


################################# Main Program ##############################


index     = 0                      # time interval index     */
inventory = MAXIMUM                # current inventory level */
demand = -1                            # amount of demand        */
order  = -1                              # amount of order         */
sum = sumOf()

#read in demands from file 
try:
  fp = open(FILENAME, "r")
except IOError:
  print("File not found")
  exit()

data = []
for line in fp:
  data.append(int(line))

fp.close()



for demand in data:
  index += 1

  if (inventory < MINIMUM):              # place an order          */
    order         = MAXIMUM - inventory
    sum.setup    += 1.0
    sum.order    += order
  
  else:                                   # no order                 */
    order         = 0  

  inventory      += order               # there is no delivery lag */
  #demand          = GetDemand(fp)

  sum.demand     += demand
  if (inventory > demand): 
    sum.holding  += (inventory - 0.5 * demand)
  else:
    sum.holding  += (inventory*inventory) / (2.0 * demand)
    sum.shortage += ((demand - inventory)*(demand-inventory)) / (2.0 * demand) #debug
  
  inventory      -= demand
#EndFor


if (inventory < MAXIMUM):               # force the final inventory to */
  order           = MAXIMUM - inventory # match the initial inventory  */
  sum.setup += 1
  sum.order      += order
  inventory      += order


print("\nfor {0:1d} time intervals with an average demand of {1:6.2f}".format(index,(sum.demand / index)))
print("and policy parameters (s, S) = ({0}, {1})\n".format(MINIMUM, MAXIMUM))
print("   average order ............ = {0:6.2f}".format(sum.order / index))
print("   setup frequency .......... = {0:6.2f}".format(sum.setup / index))
print("   average holding level .... = {0:6.2f}".format(sum.holding / index))
print("   average shortage level ... = {0:6.2f}".format(sum.shortage / index))

#C output:
# for 100 time intervals with an average demand of  29.29
# and policy parameters (s, S) = (20, 80)

#    average order ............ =  29.29
#    setup frequency .......... =   0.39
#    average holding level .... =  42.40
#    average shortage level ... =   0.25
