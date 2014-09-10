"""
Testing parallalism
mpirun -c 4 python parallel_spike.py
"""

from eqrm_code.parallel import Parallel
import eqrm_code.polygon

import pypar

def one_example():
    txt = ["yes", "no", "when", "what the", "a", "5ive!"]

    rank = pypar.rank()
    size = pypar.size()

    print "I am processor %d of %d. " % (rank, size)
    for i, ele in enumerate(txt):
        if i % size == rank:
            print "i" + str(i) + " P"+ str(rank) + " len " + str(len(ele)) + " for " + ele


def two_example():
    txt = ["yes", "no", "when", "what the", "a", "5ive!"]

    rank = pypar.rank()
    size = pypar.size()

    print
    print "I am processor %d of %d. " % (rank, size)
    for i, ele in enumerate(txt):
        if i % size == rank:
            print "i" + str(i) + " P"+ str(rank) + " len " + str(len(ele)) + " for " + ele

    pypar.finalize()

def hello():
    print "Hi ", pypar.rank()
if __name__ == '__main__':
    #hello()
    one_example()