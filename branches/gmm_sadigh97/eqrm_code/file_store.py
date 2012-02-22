"""
file_store.py

A base class that implements file store methods for NumPy arrays 
"""

import os
import tempfile

from numpy import save, load
from numpy.lib.format import open_memmap

# SAVE_METHOD
# Specifies whether a file based storage method is to be used for attributes. 
# Currently supported values:
#
# 'npy'      - numpy native binary format (1 file per attribute per Event_Set)
# None       - in memory
#
SAVE_METHOD = 'npy'

class FileStoreException(Exception):
    pass

class File_Store(object):
    """
    File_Store
    
    Implements getters and setters for the storage of NumPy arrays to file. It
    uses NumPy's native binary data format to save files to disk and reads them
    back again as an ndarray-like memmap object.
    
    Use:
    - Inherit File_Store in the class that contains the ndarrays as attributes
    - Override the attributes native getters and setters using the property function
      with the getters in this class
    - Ensure the __init__ method of the class calls File_Store's __init__ method 
      to set up the file using an identifying name (__init__ will create a unique
      filename with the name and array name given as part of the name)
    - Ensure the __del__ method of the class calls File_Store's __del__ method
      to clean up the files as the object is deleted
      
    e.g.
    class Event_Set_Data(file_store.File_Store):
    
        def __init__(self):
            super(Event_Set_Data, self).__init__('event_set_data')
    
        def __del__(self):
            super(Event_Set_Data, self).__del__()
        
        num_events = property(lambda self: self._get_file_array('num_events'), 
                              lambda self, value: self._set_file_array('num_events', value))
    
    in use:
    >>> import numpy as np
    >>> from eqrm_code.event_set_data import Event_Set_Data
    >>> data = Event_Set_Data()
    >>> data.num_events = np.random.rand(100)
    >>> data.num_events
    memmap([ 0.43213026,  0.20762537,  0.22894277,  0.62847963,  0.96151318,
            0.00375203,  0.49487985,  0.60925976,  0.65064468,  0.99760866,
            0.19795651,  0.44644592,  0.19468941,  0.3152081 ,  0.23172123,
            0.18597068,  0.15085439,  0.70180277,  0.5291986 ,  0.2273956 ,
            0.79777836,  0.13991769,  0.34723354,  0.3056998 ,  0.9250856 ,
            0.77613152,  0.5466083 ,  0.85779571,  0.35510461,  0.85456009,
            0.90607866,  0.51300493,  0.94859634,  0.03148768,  0.53839669,
            0.8552722 ,  0.24833374,  0.23522501,  0.58987406,  0.21043964,
            0.27157776,  0.34232642,  0.57128712,  0.98857091,  0.36354433,
            0.68326922,  0.48782194,  0.56147978,  0.42177197,  0.25725515,
            0.19568388,  0.81848127,  0.89879879,  0.19206585,  0.52824653,
            0.04966784,  0.9214825 ,  0.66067833,  0.87525982,  0.48795947,
            0.31004879,  0.02304321,  0.49331501,  0.42278301,  0.79691681,
            0.86813868,  0.97935636,  0.0765511 ,  0.20930933,  0.18916981,
            0.54224466,  0.85470341,  0.16694914,  0.62721499,  0.40443436,
            0.78158547,  0.03847872,  0.63289132,  0.67936138,  0.73461755,
            0.76575497,  0.49486687,  0.71410434,  0.8481302 ,  0.35516048,
            0.14276678,  0.58594872,  0.30368607,  0.37968479,  0.25581018,
            0.14636913,  0.96046498,  0.64339903,  0.59396796,  0.01239824,
            0.5415874 ,  0.63406459,  0.4296261 ,  0.27724911,  0.57388861])
    
    while object data exists
    $ ls -lh /tmp/*.npy
    -rw-r--r-- 1 ben ben 880 Feb  7 17:00 /tmp/event_set_data.num_events._x_oDyw.npy
    
    deleting the object will remove these files
    >>> del data
    
    $ ls -lh /tmp/*.npy
    ls: /tmp/*.npy: No such file or directory
    """
    
    
    def __init__(self, name, dir):
        """__init__: create a file store instance with name and dir"""
        self._name = name
        self._array_files = {}
        self._dir = dir # if this is None tempfile will use /tmp

    def __del__(self):
        """__del__: Make sure any data files are cleaned up"""
        for filename in self._array_files.values():
            os.remove(filename)
    
    def _get_numpy_binary_array(self, name):
        """Return the an memmap object as represented by the .npy file"""
        filename = self._array_files.get(name)  
        if filename is not None:
            return open_memmap(filename)
        else:
            return None
        
    def _set_numpy_binary_array(self, name, array):
        """Store the array in an .npy file"""
        if array is not None:
            filename = self._array_files.get(name)
            
            # Create and map a new file if needed
            if filename is None:
                handle, filename = tempfile.mkstemp(prefix='%s.%s.' % (self._name, name), 
                                                    suffix='.npy',
                                                    dir=self._dir)
                os.close(handle)
                self._array_files[name] = filename
                
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
            
    def _save(self, dir=None):
        """Save the associated .npy files in the given dir."""
        if len(self._array_files) > 0:
            if dir is None:
                dir = os.path.curdir
            
            # Make save dir if necessary
            save_dir = os.path.join(dir, self._name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Place each array file in the save dir
            for name, filename in self._array_files.items():
                save(os.path.join(save_dir, '%s.npy' % name), load(filename))
                
            
    def _load(self, dir=None):
        """Load the associated .npy files from the given dir into file_store 
        arrays"""
        if dir is None:
            dir = os.path.curdir
        
        load_dir = os.path.join(dir, self._name)
        if not os.path.exists(load_dir):
            raise FileStoreException("Directory %s does not exist" % load_dir)
        
        # Load each name.npy file into the file structure using
        # _set_numpy_binary_array(name, load(name.npy))
        for root,_,files in os.walk(load_dir):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext == '.npy':
                    self._set_file_array(name, load(os.path.join(root,file)))
        

