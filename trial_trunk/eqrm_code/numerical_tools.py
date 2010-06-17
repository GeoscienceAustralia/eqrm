#!/usr/bin/env python
"""

Auxiliary numerical tools

Based on numerical tools from ANUGA
"""
import types

from scipy import ndarray, array, sum, ravel, sqrt, searchsorted, sort, \
     concatenate,  arange, inner

# Getting an infinite number to use when using Numeric
INF = (array([1])/0.)[0]



def angle(v1, v2=None):
    """Compute angle between 2D vectors v1 and v2.
    
    If v2 is not specified it will default 
    to e1 (the unit vector in the x-direction)

    The angle is measured as a number in [0, 2pi] from v2 to v1.
    """
    from math import acos, pi, sqrt
  
    # Prepare two Numeric vectors
    if v2 is None:
        v2 = [1.0, 0.0] # Unit vector along the x-axis
	
    v1 = ensure_numeric(v1, float)
    v2 = ensure_numeric(v2, float)    
    
    # Normalise
    v1 = v1/sqrt(sum(v1**2))
    v2 = v2/sqrt(sum(v2**2))
   
    # Compute angle
    p = inner(v1, v2)
    c = inner(v1, normal_vector(v2)) # Projection onto normal
                                            # (negative cross product)
    
    theta = acos(p)
    
    # Correct if v1 is in quadrant 3 or 4 with respect to v2 (as the x-axis) 
    # If v2 was the unit vector [1,0] this would correspond to the test
    # if v1[1] < 0: theta = 2*pi-theta    
    # In general we use the sign of the projection onto the normal.
    if c < 0: 
       #Quadrant 3 or 4
       theta = 2*pi-theta        
       
    return theta

    
def anglediff(v0, v1):
    """Compute difference between angle of vector v0 (x0, y0) and v1 (x1, y1).
    This is used for determining the ordering of vertices,
    e.g. for checking if they are counter clockwise.

    Always return a positive value
    """

    from math import pi

    a0 = angle(v0)
    a1 = angle(v1)

    #Ensure that difference will be positive
    if a0 < a1:
        a0 += 2*pi

    return a0-a1

def normal_vector(v):
    """Normal vector to v.

    Returns vector 90 degrees counter clockwise to and of same length as v
    """
    
    return array([-v[1], v[0]], float)

    
       
def mean(x):
    """Mean value of a vector
    """
    return(float(sum(x))/len(x))


def cov(x, y=None):
    """Covariance of vectors x and y.

    If y is None: return cov(x, x) 
    """
    
    if y is None:
        y = x 

    assert(len(x)==len(y))
    N = len(x)
 
    cx = x - mean(x)  
    cy = y - mean(y)  

    p = inner(cx,cy)/N
    return(p)


def err(x, y=0, n=2, relative=True):
    """Relative error of ||x-y|| to ||y||
       n = 2:    Two norm
       n = None: Max norm

       If denominator evaluates to zero or
       if y is omitted or
       if keyword relative is False,
       absolute error is returned
    """

    x = ensure_numeric(x)
    if y:
        y = ensure_numeric(y)        

    if n == 2:
        err = norm(x-y)
        if relative is True:
            try:
                err = err/norm(y)
            except:
                pass

    else:
        err = max(abs(x-y))
        if relative is True:
            try:
                err = err/max(abs(y))    
            except:
                pass
          
    return err
  

def norm(x):
    """2-norm of x
    """
  
    y = ravel(x)
    p = sqrt(inner(y,y))
    return p
    
  
def corr(x, y=None):
    """Correlation of x and y
    If y is None return autocorrelation of x
    """

    from math import sqrt
    if y is None:
        y = x 

    varx = cov(x)
    vary = cov(y)

    if varx == 0 or vary == 0:
        C = 0
    else:  
        C = cov(x,y)/sqrt(varx * vary)   

    return(C)

	
def ensure_numeric(A, typecode = None):
    """Ensure that sequence is a Numeric array.
    Inputs:
        A: Sequence. If A is already a Numeric array it will be returned
                     unaltered
                     If not, an attempt is made to convert it to a Numeric
                     array
        A: Scalar.   Return 0-dimensional array of length 1, containing that
                     value
        A: String.   Array of ASCII values
        typecode: Numeric type. If specified, use this in the conversion.
                                If not, let Numeric decide

    This function is necessary as array(A) can cause memory overflow.
    """

    if typecode is None:
        if type(A) == ndarray:
            return A
        else:
            return array(A)
    else:
        if type(A) == ndarray:
            if A.dtype == typecode:
                return array(A)  #FIXME: Shouldn't this just return A?
            else:
                return array(A, typecode)
        else:
            import types                            ##
            if isinstance(A, types.StringType):     ##
                return array(A, dtype=int)    ##
            return array(A, typecode)
	


def histogram(a, bins, relative=False):
    """Standard histogram straight from the Numeric manual

    If relative is True, values will be normalised againts the total and
    thus represent frequencies rather than counts.
    """

    n = searchsorted(sort(a), bins)
    n = concatenate( [n, [len(a)]] )

    hist = n[1:]-n[:-1]

    if relative is True:
        hist = hist/float(sum(hist))
        
    return hist 

def create_bins(data, number_of_bins = None):
    """Safely create bins for use with histogram
    If data contains only one point or is constant, one bin will be created.
    If number_of_bins in omitted 10 bins will be created
    """

    mx = max(data)
    mn = min(data)

    if mx == mn:
        bins = array([mn])
    else:
        if number_of_bins is None:
            number_of_bins = 10
            
        bins = arange(mn, mx, (mx-mn)/number_of_bins)

    return bins


