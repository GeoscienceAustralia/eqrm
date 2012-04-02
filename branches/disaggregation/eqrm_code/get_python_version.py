
# Was going to be used in a test in util.

import os
import sys

python_version = sys.version[0:5]
number = ''.join(python_version.split('.'))

sys.exit(number) 
