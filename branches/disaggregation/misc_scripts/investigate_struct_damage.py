
# from scipy import fromfile

# struct = fromfile(file='natadelaide_structural_damage.txt',
#                   dtype=scipy.float64, sep=',')

# print "struct.shape", struct.shape
#print "struct", struct

# from scipy.io import read_array # Works, but deprecated

# struct = read_array('natadelaide_structural_damage.txt', ',')
# print "struct.shape", struct.shape

import scipy

from scipy import loadtxt

struct = loadtxt('natadelaide_structural_damage.txt', dtype=scipy.float64,
                 delimiter=',', skiprows=1)
#struct = loadtxt('cropped_nat.txt', dtype=scipy.float64,delimiter=',', skiprows=1)
print "struct.shape", struct.shape

print "struct[0,:]", struct[0,:] # Let's look at the first row

# b is the 51 values where the last column is > 0.99...
b = struct[s.nonzero(struct[:,4]>0.999777531),:]
b = b.reshape(-1,5)
