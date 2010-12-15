"""
  Title: parallel.py
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  Description: Parallel class to allow EQRM to run on a cluster.
  
  Version: $Revision: 1624 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-21 11:45:36 +1000 (Wed, 21 Apr 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
import math
from eqrm_code.output_manager import FILE_TAG_DELIMITER
import socket


class Parallel(object):
    """ Parallelise EQRM so it can run on a cluster.

    Attributes:
    rank: What is the id of this node in the cluster.
    size: How many processors are there in the cluster.
    node: name of the cluster node.
    is_parallel: True if parallel is operational
    file_tag: A string that can be added to files to identify who wrote the
      file.      
    _make_block_file: Does this node have data to write to a block
      file?  WARNING This attribute is tighly coupled to calc_lo_hi.
      It is assuming calc_lo_hi is only called with one value.
      (Assumption is currently true)
      
    """
    def __init__(self, is_parallel=True):
        """
        Use is_parallel = False to stop parallelism, eg when running
        several scenarios.
        """
        
        if is_parallel is True:
            try:
                import pypar
            except ImportError:
                self._not_parallel()
            else:
                if pypar.size() >= 2:
                    self.rank = pypar.rank()
                    self.size = pypar.size()
                    self.node = pypar.get_processor_name()
                    self.is_parallel = True
                    self.file_tag = FILE_TAG_DELIMITER + str(self.rank)
                    self.log_file_tag = FILE_TAG_DELIMITER + str(self.rank)
                else:
                    self._not_parallel()
        else:
            self._not_parallel()

            
    def calc_lo_hi(self, elements):
        """
        Calculate the low index and the high index of length elements,
        so each node can work on a section of an array.

        Args:
          elements: Lenght of array/list etc.

        Return:
        
        """
        # floor - Returns the largest integral value
        # that is not greater than x.
        L = int(math.floor(1.0*elements/self.size))
        

        M = elements - self.size*L
        
        if (self.rank < M):
            lo = self.rank*L + self.rank
            hi = lo + L + 1
        else:
            lo = self.rank*L + M
            hi = lo + L

        self.lo = lo
        self.hi = hi
        if hi == lo:
            self._make_block_file = 0
        else:
            self._make_block_file = 1

        
    def _not_parallel(self):
        """
        Set the attributes if there is only one node.
        """
        self.rank = 0
        self.size = 1
        self.node = socket.gethostname() # The host name
        self.is_parallel = False
        self.file_tag = ''
        self.log_file_tag = '-0' # this is so there is always a log-0.txt file.
            
    def barrier(self):
        """
        Synchronisation point. Makes processors wait until all 
               processors have reached this point.
        """
        if self.is_parallel is True:
            import pypar
            pypar.barrier()
      
    def calc_num_blocks(self):
        """
        pre-req: calc_lo_hi has been calculated - and only calculated once!
        """
        if self.is_parallel is True:
            import pypar
            #print "synchronise self.rank", self.rank
            if self.rank == 0:
                calc_num_blocks = self._make_block_file
                for source in range(1, self.size):
                    #print "waiting.."
                    received = pypar.receive(source)
                    #print "received", received
                    calc_num_blocks += received
                return calc_num_blocks
            else:
                #print "sending from ", self.rank
                pypar.send(self._make_block_file, 0)
                #print "sent from ", self.rank
                
    def finalize(self):
        """
        End being parallel
        """
        if self.is_parallel is True:
            import pypar
            pypar.finalize()


# this will run if eqrm_analysis.py is called from DOS prompt or double clicked
if __name__ == '__main__':
    
    sites_len = 10
    sites = range(sites_len)
    
    parra = Parallel(is_parallel=False)
    lo,hi = parra.calc_lo_hi(sites_len)
    print "lo", lo
    print "hi", hi
    print "My work", sites[lo:hi]
    parra.finalize()
