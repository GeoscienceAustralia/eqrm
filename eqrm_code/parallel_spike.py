"""
Testing parallalism
mpirun -machinefile ~/.machines.cyclone -c 4 python parallel_spike.py
"""

from eqrm_code.parallel import Parallel
import eqrm_code.polygon

import pypar

sites_len = 10
sites = range(sites_len)

para = Parallel()
para.calc_lo_hi(sites_len)
print "I am processor %d of %d on node %s. lo is %i, hi is %i" % (para.rank,
                                                                  para.size,
                                                                  para.node,
                                                                  int(para.lo),
                                                                  int(para.hi))

for i in range(para.lo, para.hi):
    print i

# Now lets
para.finalize()
