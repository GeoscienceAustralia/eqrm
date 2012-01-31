"""
file_store.py

A base class that implements file store methods for NumPy arrays 
"""

import os, glob
import tempfile
from numpy import save
from numpy.lib.format import open_memmap

# SAVE_METHOD
# Specifies whether a file based storage method is to be used for attributes. 
# Currently supported values:
#
# 'npy'      - numpy native binary format (1 file per attribute per Event_Set)
# None       - in memory
#
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
    
    def _get_numpy_binary_array(self, name):
        """Return the array stored in the named .npy file
        """
        (root, ext) = os.path.splitext(self._filename)
        filename = '%s%s%s' % (root, name, ext)
        
        if os.path.exists(filename):
            array = open_memmap(filename)
            return array
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
        if SAVE_METHOD == 'npy':
            return self._get_numpy_binary_array(name)
        else:
            return self.__dict__.get(name)
    
    def _set_file_array(self, name, array):
        if SAVE_METHOD == 'npy':
            self._set_numpy_binary_array(name, array)
        else:
            self.__dict__[name] = array

