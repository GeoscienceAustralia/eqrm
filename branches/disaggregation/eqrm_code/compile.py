"""compile.py - compile Python C-extension

   Commandline usage: 
     python compile.py <filename>

   Usage from within Python:
     import compile
     compile.compile(<filename>,..)
 
  Version: $Revision: 914 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $

   Ole Nielsen, Duncan Gray Oct 2001      
  
  Copyright 2007 by Geoscience Australia
"""     

import os, string, sys, types
from os.path import splitext

import numpy
numpyincludedirs = numpy.get_include()
I_dir = '-I"%s" ' % numpyincludedirs

def compile(FNs=None, CC=None, LD = None, SFLAG = None, verbose = 1):
  """compile(FNs=None, CC=None, LD = None, SFLAG = None):
  
     Compile FN(s) using compiler CC (e.g. mpicc), 
     Loader LD and shared flag SFLAG.
     If CC is absent use default compiler dependent on platform
     if LD is absent CC is used.
     if SFLAG is absent platform default is used
     FNs can be either one filename or a list of filenames
     In the latter case, the first will be used to name so file.
  """
  
  # Input check
  #
  assert not FNs is None, "No filename provided"

  if not type(FNs) == types.ListType:
    FNs = [FNs]


  libext = 'so' #Default extension (Unix)
  libs = ''
  version = sys.version[:3]
  
  # Determine platform and compiler
  #
  if sys.platform == 'sunos5':  #Solaris
    if CC:
      compiler = CC
    else:  
      compiler = 'gcc'
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'G'
      
  elif sys.platform == 'osf1V5':  #Compaq AlphaServer
    if CC:
      compiler = CC
    else:  
      compiler = 'cc'
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'shared'    
      
  elif sys.platform == 'linux2':  #Linux
    if CC:
      compiler = CC
    else:  
      compiler = 'gcc'
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'shared'    
      
  elif sys.platform == 'darwin':  #Mac OS X:
    if CC:
      compiler = CC
    else:  
      compiler = 'cc'
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'bundle -flat_namespace -undefined suppress'

  elif sys.platform == 'cygwin':  #Cygwin (compilation same as linux)
    if CC:
      compiler = CC
    else:  
      compiler = 'gcc'
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'shared'
      
    # As of python2.5, .pyd is the extension for python extension  
    # modules.  
    if sys.version_info[0:2] >= (2, 5):  
      libext = 'pyd'  
    else:  
      libext = 'dll' 
    libs = '/lib/python%s/config/libpython%s.dll.a' %(version,version)
      
  elif sys.platform == 'win32':  #Windows
    if CC:
      compiler = CC
    else:  
      compiler = 'gcc.exe' #Some systems require this (a security measure?) 
    if LD:
      loader = LD
    else:  
      loader = compiler
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'shared'
      
    # As of python2.5, .pyd is the extension for python extension  
    # modules.  
    if sys.version_info[0:2] >= (2, 5):  
      libext = 'pyd'  
    else:  
      libext = 'dll' 
     

    v = version.replace('.','')
    dllfilename = 'python%s.dll' %(v)
    #libs = os.path.join(sys.exec_prefix,dllfilename)
    libs, is_found = set_python_dll_path()
      
  else:
    if verbose: print "Unrecognised platform %s - revert to default"\
                %sys.platform
    
    if CC:
      compiler = CC
    else:  
      compiler = 'cc'
    if LD:
      loader = LD
    else:  
      loader = 'ld'
    if SFLAG:
      sharedflag = SFLAG
    else:  
      sharedflag = 'G'

   
       
  # Find location of include files
  #
  if sys.platform == 'win32':  #Windows
    python_include = os.path.join(sys.exec_prefix, 'include')    
  else:  
    python_include = os.path.join(os.path.join(sys.exec_prefix, 'include'),
                                  'python' + version)

  # Check existence of Python.h
  #
  headerfile = python_include + os.sep + 'Python.h'
  try:
    open(headerfile, 'r')
  except:
    raise """Did not find Python header file %s.
    Make sure files for Python C-extensions are installed. 
    In debian linux, for example, you need to install a
    package called something like python2.3-dev""" %headerfile



  #Add Python path + utilities to includelist (see ticket:31)
  #Assume there is only one 'utilities' dir under path dirs
  
  utilities_include_dir = None

   


  # Check filename(s)
  #
  object_files = ''
  for FN in FNs:        
    root, ext = os.path.splitext(FN)
    if ext == '':
      FN = FN + '.c'
    elif ext.lower() != '.c':
      raise Exception, "Unrecognised extension: " + FN
    
    try:
      open(FN, 'r')
    except:
      raise Exception, "Could not open: " + FN

    if not object_files: root1 = root  #Remember first filename        
    object_files += root + '.o '  
  
  
    # Compile
    #
    if utilities_include_dir is None:  
        s = '%s -c %s %s -I"%s" -o "%s.o" -Wall -O3'\
            %(compiler, FN, I_dir, python_include, root)

    else:
      if I_dir is None:
        s = '%s -c %s -I"%s" -I"%s" -o "%s.o" -Wall -O3'\
            %(compiler, FN, python_include, utilities_include_dir, root)
      else:
#NumPy        s = '%s -c %s -I"%s" -I"%s" -o "%s.o" -Wall -O3'\
        s = '%s -c %s %s -I"%s" -I"%s" -o "%s.o" -Wall -O3'\
            %(compiler, FN, I_dir, python_include, utilities_include_dir, root)

        

    if os.name == 'posix' and os.uname()[4] == 'x86_64':
      #Extra flags for 64 bit architectures
      #Second clause will always fail on Win32 because uname is UNIX specific
      #but won't get past first clause

      #FIXME: Which one?
      #s += ' -fPIC'
      s += ' -fPIC -m64' 
      
      
    if verbose:
      print s
    else:
      s = s + ' 2> /dev/null' #Suppress errors
  
    try:
      err = os.system(s)
      if err != 0:
          print 'Attempting to compile %s failed ' %FN 
    except:
      print 'Could not compile %s' %FN  

  
  # Make shared library (*.so or *.dll)
  if libs is "":
    s = '%s -%s %s -o %s.%s -lm' %(loader, sharedflag, object_files, root1, libext)
  else:
    s = '%s -%s %s -o %s.%s "%s" -lm' %(loader, sharedflag, object_files, root1, libext, libs)
  if verbose:
    print s
  else:
    s = s + ' 2> /dev/null' #Suppress warnings
  
  try:  
    err=os.system(s)
    if err != 0:        
        print 'Atempting to link %s failed ' %root1     
  except:
    print 'Could not link %s ' %root1
    

def can_use_C_extension(filename):
    """Determine whether specified C-extension
    can and should be used.
    """


    root, ext = splitext(filename)
    
    C=False
    if True:
        try:
            s = 'import %s' %root
            #print s
            exec(s)
        except:
            try:
                open(filename)
            except:
                msg = 'C extension %s cannot be opened' %filename
                print msg                
            else:    
                print '------- Trying to compile c-extension %s' %filename
            
                try:
                    compile(filename)
                except:
                    print 'WARNING: Could not compile C-extension %s'\
                          %filename
                else:
                    try:
                        exec('import %s' %root)
                    except:
                      print 'WARNING: Could not import C-extension %s'\
                            %filename
                    else:
                        C=True
        else:
            C=True
            
    if not C:
        pass
        print 'NOTICE: C-extension %s not used' %filename

    return C

def set_python_dll_path():
  """ Find which of the two usual hiding places the python dll is located.

  If the file can't be found, return None.

  precondition: This is only called if the OS is windows.
  """
  import sys
  from os import access, F_OK
  
  version = sys.version[:3]
  v = version.replace('.','')
  dllfilename = 'python%s.dll' %(v)
  libs = os.path.join(sys.exec_prefix,dllfilename)
  is_found = True   
  if access(libs,F_OK) == 0 :
    # Hacky - fix if you want
    libs = os.path.join(os.environ["SYSTEMROOT"]+os.sep+'system32',dllfilename)
  if access(libs,F_OK) == 0 :
    # Hacky - fix if you want
    libs = os.path.join('c:'+os.sep+'windows'+os.sep+'system32',dllfilename)
    if access(libs,F_OK) == 0 :
      # could not find the dll
      libs = os.path.join(sys.exec_prefix,dllfilename)
      is_found = False
  return libs, is_found

def check_python_dll():
  libs, is_found = set_python_dll_path()
  if not is_found:
    print "%s not found.\nPlease install.\nIt is available on the web." \
              %(libs)
    import sys; sys.exit()
    
      
if __name__ == '__main__':
  
  if sys.platform == 'win32':
    check_python_dll()
  if len(sys.argv) > 1:
      files = sys.argv[1:]
      for filename in files:
          root, ext = splitext(filename)

          if ext <> '.c':
              print 'WARNING (compile.py): Skipping %s. I only compile C-files.' %filename
      
  else:  
      #path = os.path.split(sys.argv[0])[0] or os.getcwd()
      path = '.'
      files = os.listdir(path)
      
      
  #print "files",files 
  for filename in files:
      root, ext = splitext(filename)

      if ext == '.c':
          for x in ['.dll', '.so']:
              try:
                  os.remove(root + x)
              except:
                  pass

          print '---------------------------------------'      
          print 'Trying to compile c-extension %s in %s'\
                %(filename, os.getcwd())
          compile(filename)
        

