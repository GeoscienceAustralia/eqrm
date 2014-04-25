#!/usr/bin/env python

"""
software supporting script.
"""

import os


from eqrm_code.ANUGA_utilities.system_tools import compute_checksum
from os.path import join, basename
from os import walk


def rename_recursively(root, extension, start_text, accountable):

    for dirpath, filename in identify_datafiles(root,
                                                extension,
                                                start_text,
                                                ['.svn']):

        new_filename = filename[:4] + '_' + filename[4:]
        print "new_filename", new_filename
        path_file = join(dirpath, filename)
        #write_licence(path_file,author, accountable)
        print "path_file", path_file
        new_path_file = join(dirpath, new_filename)

        commanmd = 'svn rename ' + path_file + ' ' + new_path_file
        print "commanmd", commanmd
        os.system(commanmd)
        # Wait a bit for SVN.
        sum = 0
        for i in range(1000):
            sum += i


def identify_datafiles(root,
                       extension_to_use=None,
                       start_text=None,
                       directories_to_ignore=None):
    """ Identify files that might contain data

    """

    for dirpath, dirnames, filenames in walk(root):

        # the caller can modify the dirnames list in-place (perhaps
        # using del or slice assignment), and walk() will only recurse
        # into the subdirectories whose names remain in dirnames; this
        # can be used to prune the search

        for ignore in directories_to_ignore:
            if ignore in dirnames:
                dirnames.remove(ignore)  # don't visit ignored directories

        for filename in filenames:
            # Ignore extensions that need no IP checklicence
            # print "filename to check extension", filename
            if filename.endswith(extension_to_use) and \
                    filename.startswith(start_text):
                yield dirpath, filename

#-------------------------------------------------------------
if __name__ == "__main__":
    #write_licence('no_see.gif','Duncan Gray')
    rename_recursively(join('..', 'implementation_tests', 'standard'),
                       '.txt', 'newcto'  # 'newcbedrock'
                             , 'David Robinson')
