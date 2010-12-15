

import os
from eqrm_code import util
from eqrm_code.output_manager import load_hazards

# get EQRM root path
eqrm_path = util.determine_eqrm_path()

# create paths to various sub-directories
datadir = os.path.join(eqrm_path, 'demo', 'output', 'prob_haz')
site_tag = 'newc'
soil_amp = False		# bedrock

# load the hazard info from demo\prob_haz 
SA, periods, return_p  = load_hazards(datadir, site_tag, soil_amp)

print "periods len", len(periods) 
print "return_p", len(return_p)
print "SA.shape", SA.shape # dimensions (site, periods, return period)
# the site lat's and long's can be loaded from newc_locations.txt
