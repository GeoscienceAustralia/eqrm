"""
manipulate_EQRMfiles.py contains functions to manipulate EQRM data.

CONTAINS: 
readEQRMbfile       Reads an EQRM building database file - returns fields as list
readEQRMpfile       Reads an EQRM population database file - returns fields as lists

David Robinson
1 December 2012

"""
import csv 

def writeEQRMbfile(EQRMbfile,nsites,BID, LATITUDE, LONGITUDE, STRUCTURE_CLASSIFICATION, STRUCTURE_CATEGORY, 
            HAZUS_USAGE, SUBURB, POSTCODE, PRE1989, HAZUS_STRUCTURE_CLASSIFICATION, CONTENTS_COST_DENSITY,
            BUILDING_COST_DENSITY, FLOOR_AREA, SURVEY_FACTOR, FCB_USAGE, SITE_CLASS, VS30):
    """
    This functions writes an EQRM building database file.

    INPUTS: 
    EQRMbfile  filename of EQRM building database to be created
    nsites     number of sites in the following lists 
    ++ the following lists - fileds as defined in EQRM technical documentation
            BID, LATITUDE, LONGITUDE, STRUCTURE_CLASSIFICATION, STRUCTURE_CATEGORY, 
            HAZUS_USAGE, SUBURB, POSTCODE, PRE1989, HAZUS_STRUCTURE_CLASSIFICATION, CONTENTS_COST_DENSITY,
            BUILDING_COST_DENSITY, FLOOR_AREA, SURVEY_FACTOR, FCB_USAGE, SITE_CLASS, VS30)

    """
         
    csvOut=open(EQRMbfile,'w')
    w = csv.writer(csvOut)
    w.writerow(['BID', 'LATITUDE', 'LONGITUDE', 'STRUCTURE_CLASSIFICATION', 'STRUCTURE_CATEGORY', 'HAZUS_USAGE', 
            'SUBURB', 'POSTCODE', 'PRE1989', 'HAZUS_STRUCTURE_CLASSIFICATION', 'CONTENTS_COST_DENSITY', 
            'BUILDING_COST_DENSITY', 'FLOOR_AREA', 'SURVEY_FACTOR', 'FCB_USAGE', 'SITE_CLASS', 
            'VS30']) # write the header line
    print nsites
    for j in range(0,nsites):  # Now write the data rows
        w.writerow([BID[j], LATITUDE[j],LONGITUDE[j],STRUCTURE_CLASSIFICATION[j],STRUCTURE_CATEGORY[j],HAZUS_USAGE[j],
                SUBURB[j],POSTCODE[j],PRE1989[j],HAZUS_STRUCTURE_CLASSIFICATION[j],CONTENTS_COST_DENSITY[j],
                BUILDING_COST_DENSITY[j], FLOOR_AREA[j], SURVEY_FACTOR[j], FCB_USAGE[j], SITE_CLASS[j], VS30[j]])
    csvOut.close()


def writeEQRMpfile(EQRMpfile,nsites,LATITUDE,LONGITUDE, SITE_CLASS, VS30, POPULATION):
    """
    This functions writes an EQRM population database file.

    INPUTS: 
    EQRMpfile  filename of EQRM building database to be created
    nsites     number of sites in the following lists 
    ++ the following lists - fileds as defined in EQRM technical documentation
            LATITUDE, LONGITUDE, SITE_CLASS, VS30, POPULATION

    """

    csvOut=open(EQRMpfile,'w')
    w = csv.writer(csvOut)
    w.writerow(['LATITUDE', 'LONGITUDE', 'SITE_CLASS','VS30', 'POPULATION']) # write the header line
    print nsites
    for j in range(0,nsites):  # Now write the data rows
        w.writerow([LATITUDE[j],LONGITUDE[j], SITE_CLASS[j], VS30[j], POPULATION[j]])
    csvOut.close()


def readEQRMbfile(EQRMbfile):
    """
    This function reads an EQRM building file and returns all of the fields as lists

    INPUTS: 
    EQRMbfile     filename of EQRM building database file to be read
    """

    # Initialise some lists to place the data in
    BID = list()
    LATITUDE = list()
    LONGITUDE = list()
    STRUCTURE_CLASSIFICATION = list()
    STRUCTURE_CATEGORY = list()
    HAZUS_USAGE = list()
    SUBURB = list()
    POSTCODE = list()
    PRE1989 = list()
    HAZUS_STRUCTURE_CLASSIFICATION = list()
    CONTENTS_COST_DENSITY = list()
    BUILDING_COST_DENSITY = list()
    FLOOR_AREA = list()
    SURVEY_FACTOR = list()
    FCB_USAGE = list()
    SITE_CLASS = list()
    VS30 = list()
    
# Read the EQRM building exposure database file
    count = 0
    with open(EQRMbfile, 'rbU') as f:
        reader = csv.reader(f)
        for row in reader:
            if count ==0:   # Grab the header
                header = row
                print " ===================================================  "
                print "The header is: "
                print header
                print " ===================================================  "
                print "    "
                print "USER must ensure that the above header is in the following expected format"
                print "BID"
                print "LATITUDE"
                print "LONGITUDE"
                print "STRUCTURE_CLASSIFICATION"
                print "STRUCTURE_CATEGORY"
                print "HAZUS_USAGE"
                print "SUBURB"
                print "POSTCODE"
                print "PRE1989"
                print "HAZUS_STRUCTURE_CLASSIFICATION"
                print "CONTENTS_COST_DENSITY"
                print "BUILDING_COST_DENSITY"
                print "FLOOR_AREA"
                print "SURVEY_FACTOR"
                print "FCB_USAGE"
                print "SITE_CLASS"
                print "VS30"
                print " ===================================================  "
                count = count+1
            else: # Assign data row-by-row into the lists
                BID.append(row[0])
                LATITUDE.append(row[1])
                LONGITUDE.append(row[2])
                STRUCTURE_CLASSIFICATION.append(row[3])
                STRUCTURE_CATEGORY.append(row[4])
                HAZUS_USAGE.append(row[5])
                SUBURB.append(row[6])
                POSTCODE.append(row[7])
                PRE1989.append(row[8])
                HAZUS_STRUCTURE_CLASSIFICATION.append(row[9])
                CONTENTS_COST_DENSITY.append(row[10])
                BUILDING_COST_DENSITY.append(row[11])
                FLOOR_AREA.append(row[12])
                SURVEY_FACTOR.append(row[13])
                FCB_USAGE.append(row[14])
                SITE_CLASS.append(row[15])
                VS30.append(row[16])
                count = count+1
    nsites = count-1   

    return(nsites,header,BID, LATITUDE, LONGITUDE, STRUCTURE_CLASSIFICATION, STRUCTURE_CATEGORY, 
            HAZUS_USAGE, SUBURB, POSTCODE, PRE1989, HAZUS_STRUCTURE_CLASSIFICATION, CONTENTS_COST_DENSITY,
            BUILDING_COST_DENSITY, FLOOR_AREA, SURVEY_FACTOR, FCB_USAGE, SITE_CLASS, VS30)


def readEQRMpfile(EQRMpfile):
    """
    This function reads an EQRM population file and returns all of the fields as lists

    INPUTS: 
    EQRMpfile     filename of EQRM population database file to be read
    """

    # Initialise some lists to place the data in
    LATITUDE = list()
    LONGITUDE = list()
    SITE_CLASS = list()
    VS30 = list()
    POPULATION = list()
    
# Read the EQRM building exposure database file
    count = 0
    with open(EQRMpfile, 'rbU') as f:
        reader = csv.reader(f)
        for row in reader:
            if count ==0:   # Grab the header
                header = row
                print " ===================================================  "
                print "The header is: "
                print header
                print " ===================================================  "
                print "    "
                print "USER must ensure that the above header is in the following expected format"
                print "LATITUDE"
                print "LONGITUDE"
                print "SITE_CLASS"
                print "VS30"
                print "POPULATION"
                print " ===================================================  "
                count = count+1
            else: # Assign data row-by-row into the lists
                LATITUDE.append(row[0])
                LONGITUDE.append(row[1])
                SITE_CLASS.append(row[2])
                VS30.append(row[3])
                POPULATION.append(row[4])
                count = count+1
    nsites = count-1   

    return(nsites,header, LATITUDE, LONGITUDE, SITE_CLASS, VS30, POPULATION)
