# -------------------------------------------------------------------------
# *
# * python tri.py
# * -------------------------------------------------------------------------
# */


from rngs import selectStream, plantSeeds, random
from math import log, sqrt, exp, pow


def intri(a,b,c):
    selectStream(0)

    u = random()
    variate = 0

    if (u < (c-a)/(b-a)):
        variate = a + pow((u*(b-a)*(c-a)),.5) 
    else:
        variate = b - pow(((1-u)*(b-a)*(b-c)), .5)

    return(variate)


def artri(a,b,c):
    selectStream(1)
    temp=0

    while(temp==0):
        x = a + (b - a) *random() # gen U(a,b) for x */
        S = c*random() # use mode for majorizing fn */ 

        if(x <= c):
            test = (2*x - 2*a)/((b-a)*(c-a))
        else:
            test = (2*b - 2*x)/((b-a)*(b-c))
        if (S <= test):
            return(x)


def cotri(a,b,c):
    selectStream(2)

    p1 = (c-a)/(b-a)
    u = random()
    variate = 0

    if (u < p1):
        variate = a + (c-a)*pow(random(),.5)
    else:
        variate = b - (b-c)*pow((1-random()),.5)

    return(variate)

######################################Main Program###################################

plantSeeds(123456789)

runs = 10000
a = 4
b = 8
c = 7

# generate 1000 with inverse */
invArray = [None for i in range(0,runs)]
sum = 0

for i in range(0,runs):
    invArray[i] = intri(a,b,c)
    sum += invArray[i]

invMean = sum/runs

print("The inverse technique mean is: {0:f}".format(invMean))

# generate 1000 with accept/reject */ 
arArray= [None for i in range(0,runs)]
sum = 0 

for i in range(0,runs):
    arArray[i] = artri(a,b,c)
    sum += arArray[i]

arMean = sum/runs
print("The accept/reject technique mean is: {0:f}".format(arMean))

# generate 1000 with composition */
coArray= [None for i in range(0,runs)]
sum = 0

for i in range(0,runs):
    coArray[i] = intri(a,b,c)
    sum += coArray[i]

coMean = sum/runs

print("The composition technique mean is: {0:f}".format(coMean))

print("The theoretic mean is: {0:f}".format(((a+b+c)/3.0)))

# C output:
# The inverse technique mean is: 6.329702
# The accept/reject technique mean is: 6.324475
# The composition technique mean is: 6.337426
# The theoretic mean is: 6.333333