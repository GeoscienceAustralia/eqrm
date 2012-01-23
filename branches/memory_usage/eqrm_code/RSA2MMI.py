"""Script to convert spectral acceleration values to Modified Mercalli
Intensity (MMI) scale values.
Uses formula from Atkinson and Kaka 2007 BSSA 97 (2).

Also converts EQRM output into ArcGIS friendly format by joining coordinates
with modelled ground motion.

2 output file of intensity produced, 1 capped at MMI IX, the other at MMI X
Option to include uncertainty in PSA2MMI conversions by random sampling.
Not recommended if uncertainty already included in ground motion model as
double counting of uncertainty may occur.

Usage: python RSA2MMI.py <site_loc>_locations.txt <input period = 1.0> <include uncertainty = n (y)>
Creator: Jonathan Griffin, Australia-Indonesia Facility for Disaster Reduction
Created: 26 April 2010
"""

from scipy import zeros, nonzero, log10, array

    
# Convert RSA to MMI using Atkinson and Kaka (2007) formula
# Currently only implemented for PGA, need to add for other periods.
# 
def rsa2mmi_array(data,period = 1.0):
    data = array(data)
    verbose = False
    MMI_list = []
    if period == 1.0:
        if verbose: print 'doing period ',period
        C1 = 3.23
        C2 = 1.18
        C3 = 0.57
        C4 = 2.95
        logy15 = 1.50
        sigma1 = 0.84
    elif period == 0.0:
        if verbose: print 'doing period ',period
        C1 = 2.65
        C2 = 1.39
        C3 = -1.91
        C4 = 4.09
        logy15 = 1.69
        sigma1 = 1.01
    elif period == 2.0:
        if verbose: print 'doing period ',period
        C1 = 3.72
        C2 = 1.29
        C3 = 1.99
        C4 = 3.00
        logy15 = 1.00
        sigma1 = 0.86
    elif period == 0.3:
        if verbose: print 'doing period ',period
        C1 = 2.40
        C2 = 1.36
        C3 = -1.83
        C4 = 3.56
        logy15 = 1.92
        sigma1 = 0.88
    else:
        print 'period ',period,' not implemented yet!'
        return 0    
    
    data *= 980
    MMI = zeros(data.shape)
    ind = nonzero(log10(data)<=logy15)
    MMI[ind] = C1 + C2*(log10((data[ind])))
    ind = nonzero(log10(data)>logy15)
    MMI[ind] = C3 + C4*(log10((data[ind])))
    ind = nonzero(MMI>10)
    MMI[ind] = 10
    
    # This will never have any indexes, since you can only take the log10 of a 
    # positive number, and you do log10(data) above.
    ind = nonzero(data<=0)
    MMI[ind] = 0
    
    return MMI
