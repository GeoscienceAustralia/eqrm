#!/usr/bin/python2

# modified a bit from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/277753
# (peter - added the ability to specify file names (or extensions)

import fileinput, glob, string, sys, os
from os.path import join
# replace a string in multiple files
#filesearch.py

if len(sys.argv) < 2:
    print "usage: %s search_text replace_text ext directory" % os.path.basename(sys.argv[0])
    sys.exit(0)

stext = sys.argv[1]
rtext = sys.argv[2]

    
if len(sys.argv) == 5:
    path = join(sys.argv[4],"*")
else:
    path = "*"

if len(sys.argv) > 3:
    path = path+sys.argv[3]
    
print "finding: " + stext + " replacing with: " + rtext + " in: " + path

files = glob.glob(path)
print files

for line in fileinput.input(files,inplace=1):
  lineno = 0
  lineno = string.find(line, stext)
  if lineno >0:
        line =line.replace(stext, rtext)

  sys.stdout.write(line)


