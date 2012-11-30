"""
EQRM_2_OQ contains conversion files to convert EQRM data input files 
to OpenQuake input files.

INCLUDES: 
EQRMexp_2_OQexp   EQRM exposure input => OQ exposure input
"""

#from eqrm_code import ...
import csv

def EQRMexp_2_OQexp(EQRMfile):
    """ 
    EQRMexp_2_OQexp converts an EQRM exposure database to an OQ database. It 
    works with aggregated and un-aggregated exposure databases. 

    INPUTS: 
    EQRMfile  [string] Path and filename to EQRM format input file 

    OUTPUTS: 
    OQfile    [string] path and filename to the OQ format output file

    David Robinson
    23 November 2012
    """


    # Read the EQRM input data
    with open(EQRMfile, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row
            print row[1]
