
 # ------------------------------------------------------------------------- 
 # * This is an ANSI C library that can be used to evaluate the probability 
 # * density functions (pdf's), cumulative distribution functions (cdf's), and 
 # * inverse distribution functions (idf's) for a variety of discrete and 
 # * continuous random variables.
 # *
 # * The following notational conventions are used
 # *                 x : possible value of the random variable
 # *                 u : real variable (probability) between 0.0 and 1.0 
 # *  a, b, n, p, m, s : distribution-specific parameters
 # *
 # * There are pdf's, cdf's and idf's for 6 discrete random variables
 # *
 # *      Random Variable    Range (x)  Mean         Variance
 # *
 # *      Bernoulli(p)       0..1       p            p*(1-p)
 # *      Binomial(n, p)     0..n       n*p          n*p*(1-p)
 # *      Equilikely(a, b)   a..b       (a+b)/2      ((b-a+1)*(b-a+1)-1)/12 
 # *      Geometric(p)       0...       p/(1-p)      p/((1-p)*(1-p))
 # *      Pascal(n, p)       0...       n*p/(1-p)    n*p/((1-p)*(1-p))
 # *      Poisson(m)         0...       m            m
 # *
 # * and for 7 continuous random variables
 # *
 # *      Uniform(a, b)      a < x < b  (a+b)/2      (b-a)*(b-a)/12
 # *      Exponential(m)     x > 0      m            m*m
 # *      Erlang(n, b)       x > 0      n*b          n*b*b
 # *      Normal(m, s)       all x      m            s*s
 # *      Lognormal(a, b)    x > 0         see below
 # *      Chisquare(n)       x > 0      n            2*n
 # *      Student(n)         all x      0  (n > 1)   n/(n-2)   (n > 2)
 # *
 # * For the Lognormal(a, b), the mean and variance are
 # *
 # *                        mean = Exp(a + 0.5*b*b)
 # *                    variance = (Exp(b*b) - )1*Exp(2*a + b*b)
 # *
 # * Name            : rvms.c (Random Variable ModelS)
 # * Author          : Steve Park & Dave Geyer
 # * Language        : ANSI C
 # * Latest Revision : 11-22-97
 #   Translated by   : Philip Steele 
 #   Language        : Python 3.3
 #   Latest Revision : 3/26/14
 # * ------------------------------------------------------------------------- 
 
from math import exp, log, fabs, sqrt
#from rvgs import 


TINY= 1.0e-10
SQRT2PI= 2.506628274631              # #/* sqrt(2 * pi) */

# static double pdfStandard(x)
# static double cdfStandard(x)
# static double idfStandard(u)
# static double LogGamma(a)
# static double LogBeta(a, b)
# static double InGamma(a, b)
# static double InBeta(a, b, x)


def pdfBernoulli(p,x):
  # =======================================
  # * NOTE: use 0.0 < p < 1.0 and 0 <= x <= 1
  # * =======================================
  if(x==0):
    return (1.0-p)
  else:
    return (p)

def cdfBernoulli(p,x):
  # =======================================
  # * NOTE: use 0.0 < p < 1.0 and 0 <= x <= 1 
  # * =======================================
  if(x==0):
    return (1.0-p)
  else:
    return (1)

def idfBernoulli(p,u):
  # =========================================
  # * NOTE: use 0.0 < p < 1.0 and 0.0 < u < 1.0 
  # * =========================================
  if (u < 1.0 - p):
    return(0)
  else:
    return(1)

def pdfEquilikely(a,b,x):
  # ============================================ 
  # * NOTE: use a <= x <= b 
  # * ============================================
  return (1.0 / (b - a + 1.0))

def cdfEquilikely(a,b,x):
  # ============================================
  # * NOTE: use a <= x <= b 
  # * ============================================
  return ((x - a + 1.0) / (b - a + 1.0))

def idfEquilikely(a,b,u):
  # ============================================ 
  # * NOTE: use a <= b and 0.0 < u < 1.0 
  # * ============================================

  #LIKELY NEEDS TEST
  return (a + int(u * (b - a + 1)))

def pdfBinomial(n,p,x):
  # ============================================ 
  # * NOTE: use 0 <= x <= n and 0.0 < p < 1.0 
  # * ============================================

  # TEST

  s = LogChoose(n, x)
  t = x * log(p) + (n - x) * log(1.0 - p)
  return (exp(s + t))

def cdfBinomial(n,p,x):
  # ============================================ 
  # * NOTE: use 0 <= x <= n and 0.0 < p < 1.0 
  # * ============================================
  if (x < n):
    return (1.0 - InBeta(x + 1, n - x, p))
  else:
    return (1.0)


def idfBinomial(n,p,u):
  # ================================================= 
  # * NOTE: use 0 <= n, 0.0 < p < 1.0 and 0.0 < u < 1.0 
  # * =================================================

  x = int(n * p)             #/* start searching at the mean */

  if (cdfBinomial(n, p, x) <= u):
    while (cdfBinomial(n, p, x) <= u):
      x += 1

  elif (cdfBinomial(n, p, 0) <= u):
    while (cdfBinomial(n, p, x - 1) > u):
      x -= 1
  else:
    x = 0

  return (x)


def pdfGeometric(p,x):
  # ===================================== 
  # * NOTE: use 0.0 < p < 1.0 and x >= 0 
  # * =====================================  
  return ((1.0 - p) * exp(x * log(p)))


def cdfGeometric(p,x):
  # ===================================== 
  # * NOTE: use 0.0 < p < 1.0 and x >= 0 
  # * =====================================
  return (1.0 - exp((x + 1) * log(p)))

def idfGeometric(p,u):
  # ========================================= 
  # * NOTE: use 0.0 < p < 1.0 and 0.0 < u < 1.0 
  # * =========================================
  return ((long) (log(1.0 - u) / log(p)))


def pdfPascal(n,p,x):
  # =========================================== 
  # * NOTE: use n >= 1, 0.0 < p < 1.0, and x >= 0 
  # * ===========================================
  s = LogChoose(n + x - 1, x)
  t = x * log(p) + n * log(1.0 - p)
  return (exp(s + t))

def cdfPascal(n,p,x):
  # =========================================== 
  # * NOTE: use n >= 1, 0.0 < p < 1.0, and x >= 0 
  # * ===========================================
  return (1.0 - InBeta(x + 1, n, p))

def idfPascal(n,p,u):
  # ================================================== 
  # * NOTE: use n >= 1, 0.0 < p < 1.0, and 0.0 < u < 1.0 
  # * ==================================================

  x = int(n * p / (1.0 - p))    #/* start searching at the mean */

  if (cdfPascal(n, p, x) <= u):
    while (cdfPascal(n, p, x) <= u):
      x += 1
  elif (cdfPascal(n, p, 0) <= u):
    while (cdfPascal(n, p, x - 1) > u):
      x -= 1
  else:
    x = 0

  return (x)

def pdfPoisson(m,x):
  # ===================================
  # * NOTE: use m > 0 and x >= 0 
  # * ===================================
  t = - m + x * log(m) - LogFactorial(x)
  return (exp(t))


def cdfPoisson(m,x):
  # =================================== 
  # * NOTE: use m > 0 and x >= 0 
  # * ===================================
  return (1.0 - InGamma(x + 1, m))


def idfPoisson(m,u):
  # =================================== 
  # * NOTE: use m > 0 and 0.0 < u < 1.0 
  # * ===================================
  x = int(m)                    #/* start searching at the mean */

  if (cdfPoisson(m, x) <= u):
    while (cdfPoisson(m, x) <= u):
      x += 1
  elif (cdfPoisson(m, 0) <= u):
    while (cdfPoisson(m, x - 1) > u):
      x -= 1
  else:
   x = 0

  return (x)


def pdfUniform(a, b, x):
  # =============================================== 
  # * NOTE: use a < x < b 
  # * ===============================================


  return (1.0 / (b - a))


def cdfUniform(a, b, x):
  # =============================================== 
  # * NOTE: use a < x < b 
  # * ===============================================


  return ((x - a) / (b - a))


def idfUniform(a, b, u):
  # =============================================== 
  # * NOTE: use a < b and 0.0 < u < 1.0 
  # * ===============================================


  return (a + (b - a) * u)


def pdfExponential(m, x):
  # ========================================= 
  # * NOTE: use m > 0 and x > 0 
  # * =========================================


  return ((1.0 / m) * exp(- x / m))


def cdfExponential(m, x):
  # ========================================= 
  # * NOTE: use m > 0 and x > 0 
  # * =========================================


  return (1.0 - exp(- x / m))


def idfExponential(m, u):
  # ========================================= 
  # * NOTE: use m > 0 and 0.0 < u < 1.0 
  # * =========================================


  return (- m * log(1.0 - u))


def pdfErlang(n, b, x):
  # ============================================ 
  # * NOTE: use n >= 1, b > 0, and x > 0 
  # * ============================================

  t = (n - 1) * log(x / b) - (x / b) - log(b) - LogGamma(n)
  return (exp(t))


def cdfErlang(n, b, x):
  # ============================================ 
  # * NOTE: use n >= 1, b > 0, and x > 0 
  # * ============================================
  return (InGamma(n, x / b))


def idfErlang(n, b, u):
  # ============================================ 
  # * NOTE: use n >= 1, b > 0 and 0.0 < u < 1.0 
  # * ============================================
  x = n*b
  condition = True

  while(condition == True):             #/* use Newton-Raphson iteration */
    t = x
    x = t + (u - cdfErlang(n, b, t)) / pdfErlang(n, b, t)
    if (x <= 0.0):
      x = 0.5 * t
    condition = (fabs(x - t) >= TINY)

  return (x)

def pdfStandard(x):
  # =================================== 
  # * NOTE: x can be any value 
  # * ===================================


  return (exp(- 0.5 * x * x) / SQRT2PI)


def cdfStandard(x):
  # =================================== 
  # * NOTE: x can be any value 
  # * ===================================

  t = InGamma(0.5, 0.5 * x * x)
  if (x < 0.0):
    return (0.5 * (1.0 - t))
  else:
    return (0.5 * (1.0 + t))


def idfStandard(u):
  # =================================== 
  # * NOTE: 0.0 < u < 1.0 
  # * ===================================


  t = 0.0
  x = 0.0                    #/* initialize to the mean, then  */
  condition = True

  while(condition == True):         #/* use Newton-Raphson iteration  */
    t = x
    x = t + (u - cdfStandard(t)) / pdfStandard(t)
    condition = (fabs(x - t) >= TINY)
  
  return (x)


def pdfNormal(m, s, x):
  # ============================================== 
  # * NOTE: x and m can be any value, but s > 0.0 
  # * =============================================

  t = (x - m) / s

  return (pdfStandard(t) / s)


def cdfNormal(m, s, x):
  # ============================================== 
  # * NOTE: x and m can be any value, but s > 0.0 
  # * ==============================================
  t = (x - m) / s

  return (cdfStandard(t))


def idfNormal(m, s, u):
  # ======================================================= 
  # * NOTE: m can be any value, but s > 0.0 and 0.0 < u < 1.0 
  # * =======================================================


  return (m + s * idfStandard(u))


def pdfLognormal(a, b, x):
  # =================================================== 
  # * NOTE: a can have any value, but b > 0.0 and x > 0.0 
  # * ===================================================

  t = (log(x) - a) / b

  return (pdfStandard(t) / (b * x))


def cdfLognormal(a, b, x):
  # =================================================== 
  # * NOTE: a can have any value, but b > 0.0 and x > 0.0 
  # * ===================================================


  t = (log(x) - a) / b

  return (cdfStandard(t))


def idfLognormal(a, b, u):
  # ========================================================= 
  # * NOTE: a can have any value, but b > 0.0 and 0.0 < u < 1.0 
  # * =========================================================

  t = a + b * idfStandard(u)
  return (exp(t))


def pdfChisquare(n, x):
  # ===================================== 
  # * NOTE: use n >= 1 and x > 0.0 
  # * =====================================
  t= n/2.0
  s = n / 2.0

  t = (s - 1.0) * log(x / 2.0) - (x / 2.0) - log(2.0) - LogGamma(s)
  return (exp(t))


def cdfChisquare(n, x):
  # ===================================== 
  # * NOTE: use n >= 1 and x > 0.0 
  # * ====================================

  return (InGamma(n / 2.0, x / 2))


def idfChisquare(n, u):
  # ===================================== 
  # * NOTE: use n >= 1 and 0.0 < u < 1.0 
  # * ===================================== 
  x = n                         #/* initialize to the mean, then */
  condition = True

  while(condition == True):              #/* use Newton-Raphson iteration */
    t = x
    x = t + (u - cdfChisquare(n, t)) / pdfChisquare(n, t)
    if (x <= 0.0):
      x = 0.5 * t
    condition = (fabs(x - t) >= TINY)

  return (x)


def pdfStudent(n, x):
  # =================================== 
  # * NOTE: use n >= 1 and x > 0.0 
  # * ===================================

  s = -0.5 * (n + 1) * log(1.0 + ((x * x) / float(n)))
  t = -1*LogBeta(0.5, n / 2.0)
  return (exp(s + t) / sqrt(float(n)))


def cdfStudent(n, x):
  # =================================== 
  # * NOTE: use n >= 1 and x > 0.0 
  # * ===================================

  t = (x * x) / (n + x * x)
  s = InBeta(0.5, n / 2.0, t)
  if (x >= 0.0):
    return (0.5 * (1.0 + s))
  else:
    return (0.5 * (1.0 - s))


def idfStudent(n, u):
  # =================================== 
  # * NOTE: use n >= 1 and 0.0 < u < 1.0 
  # * ===================================
  t = 0.0 
  x = 0.0                       #/* initialize to the mean, then */
  condition = True

  while(condition == True):                #/* use Newton-Raphson iteration */
    t = x
    # print("t is set to "+ t)
    x = t + (u - cdfStudent(n, t)) / pdfStudent(n, t)
    # print("x is set to "+x)
    # print(fabs(x-t))
    condition = (fabs(x - t) >= TINY)

  return (x)


 # ===================================================================
 # * The six functions that follow are a 'special function' mini-library
 # * used to support the evaluation of pdf, cdf and idf functions.
 # * ===================================================================
 

def LogGamma(a):
  # ======================================================================== 
  # * LogGamma returns the natural log of the gamma function.
  # * NOTE: use a > 0.0 
  # *
  # * The algorithm used to evaluate the natural log of the gamma function is
  # * based on an approximation by C. Lanczos, SIAM J. Numerical Analysis, B,
  # * vol 1, 1964.  The constants have been selected to yield a relative error
  # * which is less than 2.0e-10 for all positive values of the parameter a.    
  # * ======================================================================== 

  s = []
  s.append(76.180091729406 / a)
  s.append(-86.505320327112 / (a + 1.0))
  s.append(24.014098222230 / (a + 2.0))
  s.append(-1.231739516140 / (a + 3.0))
  s.append(0.001208580030 / (a + 4.0))
  s.append(-0.000005363820 / (a + 5.0))
  sum = 1.000000000178

  for i in range(0,6): 
    sum += s[i]

  temp = (a - 0.5) * log(a + 4.5) - (a + 4.5) + log(SQRT2PI * sum)
  return (temp)

def LogFactorial(n):
  # ==================================================================
  # * LogFactorial(n) returns the natural log of n!
  # * NOTE: use n >= 0
  # *
  # * The algorithm used to evaluate the natural log of n! is based on a
  # * simple equation which relates the gamma and factorial functions.
  # * ==================================================================
  return (LogGamma(n + 1))

def LogBeta(a,b):
  # ======================================================================
  # * LogBeta returns the natural log of the beta function.
  # * NOTE: use a > 0.0 and b > 0.0
  # *
  # * The algorithm used to evaluate the natural log of the beta function is 
  # * based on a simple equation which relates the gamma and beta functions.
  # *
  return (LogGamma(a) + LogGamma(b) - LogGamma(a + b))

def LogChoose(n,m):
  # ========================================================================
  # * LogChoose returns the natural log of the binomial coefficient C(n,m).
  # * NOTE: use 0 <= m <= n
  # *
  # * The algorithm used to evaluate the natural log of a binomial coefficient
  # * is based on a simple equation which relates the beta function to a
  # * binomial coefficient.
  # * ========================================================================

  if (m > 0):
    return (-LogBeta(m, n - m + 1) - log(m))
  else:
    return (0.0)


def InGamma(a,x):
  # ========================================================================
  # * Evaluates the incomplete gamma function.
  # * NOTE: use a > 0.0 and x >= 0.0
  # *
  # * The algorithm used to evaluate the incomplete gamma function is based on
  # * Algorithm AS 32, J. Applied Statistics, 1970, by G. P. Bhattacharjee.
  # * See also equations 6.5.29 and 6.5.31 in the Handbook of Mathematical
  # * Functions, Abramowitz and Stegum (editors).  The absolute error is less 
  # * than 1e-10 for all non-negative values of x.
  # * ========================================================================

  if (x > 0.0):
    factor = exp(-1*x + a*log(x) - LogGamma(a))
  else:
    factor = 0.0

  if (x < a + 1.0):                  ##/* evaluate as an infinite series - */
    t = a                        ##/* A & S equation 6.5.29            */
    term = 1.0 / a
    sum  = term
    while (term >= TINY * sum):     ##/* sum until 'term' is small */
      t += 1
      term = term*(x / t)
      sum  += term
    #EndWhile 
    return (factor * sum)
   
  else:                              ##/* evaluate as a continued fraction - */
    p = [0.0,1.0, -1]                       ##/* A & S eqn 6.5.31 with the extended */
    q = [1.0,x, -1]                       ##/* pattern 2-a, 2, 3-a, 3, 4-a, 4,... */
                                     ##/* - see also A & S sec 3.10, eqn (3) */
    f = p[1] / q[1]
    n = 0

    condition = True
    while(condition == True):      ##/* recursively generate the continued */
      g  = f                        ##/* fraction 'f' until two consecutive */
      n += 1                           ##/* values are small                   */
      if ((n % 2) > 0):
        c=[(((n + 1) / 2.0) - a), 1]
      
      else:
        c=[(n / 2.0),x]
      
      p[2] = (c[1] * p[1] + c[0] * p[0])
      q[2] = (c[1] * q[1] + c[0] * q[0])

      if (q[2] != 0.0):             ##/* rescale to avoid overflow */
        p[0] = p[1] / q[2]
        q[0] = q[1] / q[2]
        p[1] = p[2] / q[2]
        q[1] = 1.0
        f = p[1]
      
      condition = (fabs(f - g) >= TINY) or (q[1] != 1.0)

    return (1.0 - factor * f)
   


def InBeta(a,b,x):
  # ======================================================================= 
  # * Evaluates the incomplete beta function.
  # * NOTE: use a > 0.0, b > 0.0 and 0.0 <= x <= 1.0
  # *
  # * The algorithm used to evaluate the incomplete beta function is based on
  # * equation 26.5.8 in the Handbook of Mathematical Functions, Abramowitz
  # * and Stegum (editors).  The absolute error is less than 1e-10 for all x
  # * between 0 and 1.
  # * =======================================================================

  if (x > (a + 1.0) / (a + b + 1.0)): # #/* to accelerate convergence   */
    swap = 1                          ##/* complement x and swap a & b */
    x    = 1.0 - x
    t    = a
    a    = b
    b    = t
  else:                                 ##/* do nothing */
    swap = 0

  if (x > 0):
    factor = exp(a * log(x) + b * log(1.0 - x) - LogBeta(a,b)) / a
  else:
    factor = 0.0
  
  p = [0.0,1.0, -1]
  q = [1.0,1.0, -1]
  f = p[1] / q[1]
  n = 0

  condition = True

  while (condition==True):                  ##/* recursively generate the continued */
    g = f                           ##/* fraction 'f' until two consecutive */
    n += 1                          ##/* values are small                   */

    if ((n % 2) > 0):
      t = (n - 1) / 2.0
      c = -(a + t) * (a + b + t) * x / ((a + n - 1.0) * (a + n))
    else:
      t = n / 2.0
      c = t * (b - t) * x / ((a + n - 1.0) * (a + n))
    
    p[2] = (p[1] + c * p[0])
    q[2] = (q[1] + c * q[0])
    if (q[2] != 0.0):               ##/* rescale to avoid overflow */
      p[0] = p[1] / q[2]
      q[0] = q[1] / q[2]
      p[1] = p[2] / q[2]
      q[1] = 1.0
      f    = p[1]


    condition = ((fabs(f - g) >= TINY) or (q[1] != 1.0))
  #endWhile


  if (swap == 1): 
    return (1.0 - factor * f)
  else:
    return (factor * f)


# C output:
# IDFSTU(10,.8) is 0.879058 - PASS
# IDFStud(10,.975) is 2.228139 - PASS
# IDFStud(100,.975) is 1.983972 - PASS
# IDFchisq(10,.5) is 9.341818 - PASS
# IDFchisq(15,.8) is 19.310657 - PASS
# IDFerlang(16,4,.878) is 82.934761 - PASS
# IDFerlang(20,7,.113) is 103.476309 - PASS
# IDFpoisson(16,.878) is 21.000000 - PASS
# IDFpoisson(19,.231) is 16.000000 - PASS
# IDFNorm(9,2,.66) is 9.824926 - PASS
# IDFNorm(-19,3.4,.81) is -16.015153 - PASS
# idfPascal(23,.11,.90) is 5.000000 - PASS
# idfPascal(6,.5,.5) is 6.000000 - PASS
# idfBinomial(23,.11,.90) is 5.000000 - PASS
# idfBinomial(6,.5,.5) is 3.000000 - PASS