This directory contains the local colourmaps that may be referred to
simply by the filename minus the '.cpt' extension.  For instance, on
a call to a plot routine, there is usually a 'colourmap=<name>' parameter.
The <name> may be one of the built-in GMT colourmaps *or* one of the
filenames here minus the extension.  For instance, you could pass
'colourmap=hazmap' and use the hazmap.cpt file in this directory.

When creating new colourmaps here, first check that the name you are
going to use isn't already used by GMT.  Just execute the command
'grd2cpt' to see the GMT list.  If your filename matches one of the
GMT colourmap names, the GMT colourmap will be used, not yours.

All files here should have lowercase names.  The code that looks in this
directory makes a lowercase version of the user name and looks for a
matching file.  Files with one or more uppercase characters will be
ignored!  On Windows, of course, this isn't true!!

There is one naming convention that should be followed here.  If you
have a colourmap file 'fred.cpt' with a particular colour sweep from
low to high, then a colormap with the same colour sweep but from high
to low (ie, reversed) should be called 'fredr.cpt'.
