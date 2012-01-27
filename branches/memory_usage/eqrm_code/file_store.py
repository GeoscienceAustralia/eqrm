"""
file_store.py

A base class that implements file store methods for NumPy arrays 
"""

import os, glob
import tempfile
from numpy import save, load

from eqrm_code.ANUGA_utilities import log

# SAVE_METHOD
# Specifies whether a file based storage method is to be used for attributes. 
# Currently supported values:
#
# 'npy'      - numpy native binary format (1 file per attribute per Event_Set)
# 'pytables' - PyTables hdf5 file (1 file per Event_Set)
# None       - in memory
#
SAVE_METHOD = None
try:
    import tables
    SAVE_METHOD = 'pytables'
except ImportError:
    # If pytables is unavailable, fall back to npy
    log.info('Event_Set - pytables not available, using numpy binary format for dataset storage')
    SAVE_METHOD = 'npy'

class File_Store(object):
    
    def __init__(self, name):
        if SAVE_METHOD is not None:
            self._filename = tempfile.mktemp(prefix='%s_' % name, suffix='.%s' % SAVE_METHOD)

    def __del__(self):
        """__del__ : Make sure file data is cleaned up
        """
        if SAVE_METHOD is not None:
            (root, ext) = os.path.splitext(self._filename)
            for filename in glob.glob('%s*%s' % (root, ext)) :
                os.remove( filename ) 
    
    def _get_pytables_array(self, name):
        """Return the PyTables node with a given name. This should simply be 
        a numpy array
        """
        try:
            f = tables.openFile(self._filename)
            return f.getNode(f.root, name)[:]
        except:
            return None
        finally:
            f.close()

    def _set_pytables_array(self, name, array):
        """Create a PyTables array from the numpy array with a given name, 
        removing an existing node with the same name if necessary
        """ 
        f = tables.openFile(self._filename, 'a')
        # Remove existing node if required
        try:
            f.removeNode(f.root, name, True)
        except:
            pass
        # Create one
        if array is not None:
            f.createArray(f.root, name, array)
            
        f.close()
    
    def _get_numpy_binary_array(self, name):
        """Return the array stored in the named .npy file
        """
        (root, ext) = os.path.splitext(self._filename)
        filename = '%s%s%s' % (root, name, ext)
        
        if os.path.exists(filename):
            return load(filename)
        else:
            return None
    
    def _set_numpy_binary_array(self, name, array):
        """Store the array in the .npy file using name as part of the filename
        """
        if array is not None:
            (root, ext) = os.path.splitext(self._filename)
            filename = '%s%s%s' % (root, name, ext)
            save(filename, array)
        
    def _get_file_array(self, name):
        if SAVE_METHOD == 'pytables':
            return self._get_pytables_array(name)
        elif SAVE_METHOD == 'npy':
            return self._get_numpy_binary_array(name)
        else:
            return self.__dict__.get(name)
    
    def _set_file_array(self, name, array):
        if SAVE_METHOD == 'pytables':
            self._set_pytables_array(name, array)
        elif SAVE_METHOD == 'npy':
            self._set_numpy_binary_array(name, array)
        else:
            self.__dict__[name] = array