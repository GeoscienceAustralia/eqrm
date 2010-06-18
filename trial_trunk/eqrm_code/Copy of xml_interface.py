"""
 Title: xml_interface.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           
  Description: Class to access XML information
 
  Version: $Revision: 1005 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-07-08 16:21:56 +1000 (Wed, 08 Jul 2009) $
  
  Copyright 2007 by Geoscience Australia
"""


from scipy import array,NaN
        
class Xml_Interface(object):
    def __init__(self,node=None,string=None,filename=None,dom=None):
        """        
        supports:
        node['child'] => returns a list of all child nodes named 'child'.

        node.attributes => return a dictionary of all attributes of the node
        node.array => turn the node value into an float array
        

    
        Note, if you don't know xm:
            xml nodes have both children (which have names, and an order),
            attributes (which have values), and values (the main text).

            Example:
                (in python, not xml, but highlighting the way xml works)
                
                node0
                    attributes = {dtype:float,size:10}
                    children
                        [
                        'alice' => node1
                        'bob' => node2
                        'alice' => node3 (yes, same named nodes are legal)
                        'charlie' => node4
                        ]
                    value = '1,2,3,4,5,6,7,8,9,0'
        """
        if dom is None:
            import xml.dom.minidom as dom
        self.dom = dom

        if node is not None: self.xml_node = node
        elif string is not None: self.parse_string(string)
        elif filename is not None: self.parse_file(filename)
    
    def parse_string(self,string):
        self.xml_node=self.dom.parseString(string)
        return
    
    def parse_file(self,filename):
        self.xml_node=self.dom.parse(filename)
        return
    
    def __getitem__(self,item_name):
        node_list = self.xml_node.getElementsByTagName(item_name)
        return [Xml_Interface(node=node) for node in node_list]
    
    def __attributes(self):
        get_item = self.xml_node.attributes.getNamedItem
        #get_item is now a shortcut for xml_node.attributes.getNamedItem
        attributes_dictionary = {}
        for key in self.xml_node.attributes.keys():
            attributes_dictionary[str(key)] = str(get_item(key).value)
        return attributes_dictionary

    def keys(self):
        node_list = self.xml_node.childNodes
        keys={}
        for node in node_list:
            try:
                name=node.tagName
                keys[name]=None
            except AttributeError:
                pass
        return keys.keys()

    def __array(self):
        string = self.xml_node.firstChild.nodeValue        
        #In one ugly step. 5.1.3

        def _float(x):
            try:
                x=float(x)
            except:
                if x=='NaN':
                    x=NaN
                else:
                    raise
            return x
        
        L=[tuple(map(_float,pair.split())) for pair in string.split('\n')]
        list_of_tuples = L
        """        
        #or (a bit slower)
        list_of_strings = string.split('\n')
        #split it up into small strings
        
        list_of_lists = [coordinate.split() for coordinate in list_of_strings]
        #split the small strings (coordinates) into ['lat','long'] lists
        
        list_of_lists = [map(float,coordinate) for coordinate in list_of_lists]
        #coordintates into [lat,long] lists
        
        list_of_tuples = [tuple(coordinate) for coordinate in list_of_lists]
        #coordintates into (lat,long)
        
        
        #or 
        list_of_tuples=[]
        for coordinate in string.split('\n')[1:-1]:
            coordinate = coordinate.split()
            coordinate = (float(coordinate[0]),float(coordinate[1]))
            list_of_tuples.append(coordinate)
        """
        list_of_tuples=[t for t in list_of_tuples if len(t)>0]
        # Chomp out the empty lines
        return array(list_of_tuples)
    
    attributes = property(__attributes)
    array = property(__array)
    
    def unlink(self):
        self.xml_node.unlink()
