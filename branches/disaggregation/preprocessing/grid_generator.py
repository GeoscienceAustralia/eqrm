def generate_grid(regolith_polygon_filename,site_tag,outputdir,nlats,nlons,eqrm_dir='..'):
    #fname_in = regolith polygon file (full path)
    site_polygons,polygon_site_classes=site_model_from_xml(
        regolith_polygon_filename)

    max_lat=max([polygon[:,0].max() for polygon in site_polygons]) 
    max_lon=max([polygon[:,1].max() for polygon in site_polygons])
    min_lat=min([polygon[:,0].min() for polygon in site_polygons])
    min_lon=min([polygon[:,1].min() for polygon in site_polygons])
    
    print 'max_lon,max_lat,min_lon,min_lat'
    print max_lon,max_lat,min_lon,min_lat
    from scipy import mgrid
    lon,lat=mgrid[min_lon:max_lon:nlons*1j,min_lat:max_lat:nlats*1j]
    lat.resize(lat.size) # make it 1D
    lon.resize(lon.size) # make it 1D
    print 'lat',lat,lat.shape
    print 'lon',lon,lon.shape

    site_class=populate(site_polygons,polygon_site_classes,lat,lon)
    out_file=outputdir+site_tag+'_par_site_uniform.csv'
    out_file=open(out_file,'w')
    out_file.write('LATITUDE,LONGITUDE,SITE_CLASS\n')
    for i in range(len(lat)):
        if site_class[i]!='':
            out_file.write(str(lat[i])+','+str(lon[i])+','+site_class[i]+'\n')
    out_file.close()
            
def populate(site_polygons,polygon_site_classes,lat,lon):
    from polygon import is_inside_polygon
    site_class=['' for point in lat]    
    # populate properties
    for i,polygon in enumerate(site_polygons):
        for j in range(len(lat)):
            point=lat[j],lon[j],
            if is_inside_polygon(point,polygon):
                #print polygon,point,'hit'
                site_class[j]=polygon_site_classes[i]
    return site_class
            
    
def site_model_from_xml(regolith_polygon_filename, eqrm_dir='..'):
    import sys   # imports important system function for use in Python
    if not eqrm_dir+'/eqrm_code/' in sys.path:  # adds the EQRM code subdirectory to the PATH
        sys.path.append(eqrm_dir+'/eqrm_code/')
    from eqrm_code.xml_interface import Xml_Interface
    from scipy import array

    doc=Xml_Interface(filename=regolith_polygon_filename)
    xml_source_model=doc['site_class_polygons'][0]
    # opened the xml source_polygon_filename
    site_polygons=[]
    polygon_site_classes=[]
    xml_polygons = doc['site_class_polygon']  # get a list of xml polygons
    for xml_polygon in xml_polygons:
        boundary = xml_polygon.array
        site_class=xml_polygon.attributes['site_class']        
        # make the polygon an array
        polygon=array(boundary)
        site_polygons.append(polygon)
        polygon_site_classes.append(site_class)
    doc.unlink()
    return site_polygons,polygon_site_classes


if __name__ == '__main__':
    from sys import argv
    #from os import sep
    site_tag=argv[1]
    input_dir=argv[2]
    output_dir=argv[3]
    nlats=int(argv[4])
    nlons=int(argv[5])
    sep='/'

    input_dir=input_dir.replace('\\',sep)
    
    output_dir=output_dir.replace('\\',sep)
    
    if not input_dir[-1]==sep:
        input_dir=input_dir+sep
    if not output_dir[-1]==sep:
        output_dir=output_dir+sep
    
    generate_grid(input_dir+site_tag+'_par_site_class_polys.xml',
                  site_tag,output_dir,nlats,nlons)
    
