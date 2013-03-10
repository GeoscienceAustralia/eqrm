"""
EQRM_2_OQ contains conversion files to convert EQRM data input files 
to OpenQuake input files.

CONTAINS: 
EQRMbexp_2_OQbexp   EQRM exposure input => OQ exposure input
EQRMpexp_2_OQpexp   EQRM exposure input => OQ exposure input

"""

#from eqrm_code import ...
import csv
from misc_scripts import manipulate_EQRMfiles


def EQRMbexp_2_OQbexp(EQRMbfile,OQ_bfile,textinfo):
    """ 
    EQRMbexp_2_OQbexp converts an EQRM building exposure database to an OQ database. It 
    works with aggregated and un-aggregated exposure databases. 

    INPUTS: 
    EQRMfile  [string] Path and filename to EQRM format input file 
    OQfile    [string] path and filename to the OQ format output file
    textinfo  [string] information describing file (e.g. 'ENB_agg') 

    David Robinson
    23 November 2012
    """

    # First let's raed the EQRM building database file data
    (nsites,header,BID, LATITUDE, LONGITUDE, STRUCTURE_CLASSIFICATION, STRUCTURE_CATEGORY, 
            HAZUS_USAGE, SUBURB, POSTCODE, PRE1989, HAZUS_STRUCTURE_CLASSIFICATION, CONTENTS_COST_DENSITY,
            BUILDING_COST_DENSITY, FLOOR_AREA, SURVEY_FACTOR, FCB_USAGE, SITE_CLASS,
            VS30) = manipulate_EQRMfiles.readEQRMbfile(EQRMbfile)
            

    # Now let's create the OQ building exposure dataset
    
    OQ_bfile_FID = open(OQ_bfile, 'w')
    # Write header for the xml file 
    OQ_bfile_FID.write('<exposurePortfolio gml:id="ep">\n')
    OQ_bfile_FID.write('    <exposureList gml:id="'+textinfo+'" assetCategory="buildings" units="Currency: AskMatt??">\n')
    OQ_bfile_FID.write('    <gml:description> '+textinfo+' </gml:description>\n')
    #Now let's write in the assets
    for j in range(0,nsites):  # loop over individual assets
        #First compute the total value of all assets at the site
        TotalValue = float(FLOOR_AREA[j])*float(SURVEY_FACTOR[j])*float(BUILDING_COST_DENSITY[j])
        # Now write the asset into teh xml file
        OQ_bfile_FID.write('        <assetDefinition gml:id="'+BID[j]+'">\n')
        OQ_bfile_FID.write('            <site>\n')
        OQ_bfile_FID.write('               <gml:Point srsName="AskMatt??">\n')
        OQ_bfile_FID.write('               <gml:pos>'+LATITUDE[j]+' '+LONGITUDE[j]+'</gml:pos>\n')
        OQ_bfile_FID.write('               </gml:Point>\n')
        OQ_bfile_FID.write('           </site>\n')
        OQ_bfile_FID.write('            <taxonomy>'+STRUCTURE_CLASSIFICATION[j]+'</taxonomy>\n')
        OQ_bfile_FID.write('            <assetValue> '+str(TotalValue)+' </assetValue>\n')
        OQ_bfile_FID.write('       </assetDefinition\n')
    #Now let's finish the file off
    OQ_bfile_FID.write('    </exposureList>\n')
    OQ_bfile_FID.write('</exposurePortfolio>\n')
    OQ_bfile_FID.close()


def EQRMpexp_2_OQpexp(EQRMpfile,OQ_pfile, textinfo):
    """ 
    EQRMpexp_2_OQpexp converts an EQRM population exposure database to an OQ database. It 
    works with aggregated and un-aggregated population databases. 

    INPUTS: 
    EQRMfile  [string] Path and filename to EQRM format input file 
    OQfile    [string] path and filename to the OQ format output file
    textinfo  [string] information describing file (e.g. 'ENB_agg')    

    David Robinson
    1 December 2012
    """

    # First let's raed the EQRM poulation database file data
    (nsites,header,LATITUDE, LONGITUDE, SITE_CLASS, VS30,POPULATION) = manipulate_EQRMfiles.readEQRMpfile(EQRMpfile)
            

    # Now let's create the OQ building exposure dataset
    
    OQ_bfile_FID = open(OQ_pfile, 'w')
    # Write header for the xml file 
    OQ_bfile_FID.write('<exposurePortfolio gml:id="ep">\n')
    OQ_bfile_FID.write('    <exposureList gml:id="'+textinfo+'" assetCategory="Populations" units="NumPeopleAtSite">\n')
    OQ_bfile_FID.write('    <gml:description> POPULATION in '+textinfo+'</gml:description>\n')
    #Now let's write in the assets
    for j in range(0,nsites):  # loop over individual assets
        # Now write the asset into teh xml file
        OQ_bfile_FID.write('        <assetDefinition gml:id="'+str(j)+'">\n')
        OQ_bfile_FID.write('            <site>\n')
        OQ_bfile_FID.write('               <gml:Point srsName="AskMatt??">\n')
        OQ_bfile_FID.write('               <gml:pos>'+LATITUDE[j]+' '+LONGITUDE[j]+'</gml:pos>\n')
        OQ_bfile_FID.write('               </gml:Point>\n')
        OQ_bfile_FID.write('           </site>\n')
        OQ_bfile_FID.write('            <taxonomy>'+"EQRM_Missing?? - TALK2DG"+'</taxonomy>\n')
        OQ_bfile_FID.write('            <assetValue> '+POPULATION[j]+' </assetValue>\n')
        OQ_bfile_FID.write('       </assetDefinition\n')
    #Now let's finish the file off
    OQ_bfile_FID.write('    </exposureList>\n')
    OQ_bfile_FID.write('</exposurePortfolio>\n')
    OQ_bfile_FID.close()
