
# # -------------------------------------------------------------------------
#  * This program simulates a single-server FIFO service node using arrival
#  * times and service times read from a text file.  The server is assumed
#  * to be idle when the first job arrives.  All jobs are processed completely
#  * so that the server is again idle at the end of the simulation.   The
#  * output statistics are the average interarrival time, average service
#  * time, the average delay in the queue, and the average wait in the service 
#  * node. 
#  *
#  * Name              : ssq1.c  (Single Server Queue, version 1)
#  * Authors           : Steve Park & Dave Geyer
#  * Language          : ANSI C
#  * Latest Revision   : 9-01-98
#  * Compile with      : gcc ssq1.c 
#    Translated by   : Philip Steele 
#    Language        : Python 3.3
#    Latest Revision : 3/26/14
#  * ------------------------------------------------------------------------- 
#  */
                           

FILENAME = "ssq1.dat"                  # input data file */
START = 0.0

class sumOf:
  delay = 0.0  #delay times
  wait = 0.0 #wait times
  service = 0.0 #service times
  interarrival = -1.0 #interarrival times 

###########################Main Program################################

#read in arrivals and service times from file 
try:
  fp = open(FILENAME, "r")
except IOError:
  print("File not found")
  exit()

arrivals = []
services = []

for line in fp:
  arrivals.append(float(line.split()[0]))
  services.append(float(line.split()[1]))

fp.close()

index = 0                        # job index            */
arrival = START                    # arrival time         */
delay = -1                               # delay in queue       */
service = -1                             # service time         */
wait = -1                                 # delay + service      */
departure = START                    # departure time       */
sum = sumOf()


for i in range(0,len(arrivals)):
  index += 1
  arrival      = arrivals[i]  #debug
  if (arrival < departure): 
    delay      = departure - arrival        # delay in queue    */
  else: 
    delay      = 0.0                        # no delay          */
  service      = services[i] #GetService(fp)
  wait         = delay + service
  departure    = arrival + wait             # time of departure */
  sum.delay   += delay
  sum.wait    += wait
  sum.service += service
#EndFor

sum.interarrival = arrival - START

print("\nfor {0:1d} jobs".format(index))
print("   average interarrival time = {0:6.2f}".format(sum.interarrival / index))
print("   average service time .... = {0:6.2f}".format(sum.service / index))
print("   average delay ........... = {0:6.2f}".format(sum.delay / index))
print("   average wait ............ = {0:6.2f}".format(sum.wait / index))


#C output:
# for 1000 jobs
#    average interarrival time =   9.87
#    average service time .... =   7.12
#    average delay ........... =  18.59
#    average wait ............ =  25.72