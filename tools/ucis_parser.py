import xml.etree.ElementTree as ET

"""
Description of the UCIS DB hierarchy generated by the current FC4SC implementation:

UCIS top level element
|
-> instanceCoverages [0:n]
   |  moduleName : name of the covergroup type
   |
   -> cgInstance [0:n]
      |  name : name of the covergroup instance
      |
      -> coverpoint [0:n]
      |  |  name : name of the coverpoint
      |  |
      |  -> coverpointBin [0:n]
      |     | name : name of the bin
      |     | type : the type of bin (default/ignore/illegal)
      |     |
      |     -> range [0:n]
      |        | from : start value of the interval
      |        | to   : end value of the interval
      |        |
      |        -> contents 
      |           | coverageCount : the number of hits registered in this interval
      |           0
      | 
      -> cross [0:n]
         | name : name of the cross
         |
         -> crossBin [0:n]
            | name : name of the cross bin
            | 
            -> index
            -> index 
            .
            .     Number of indexes = number of crossed coverpoints
            .
            -> index  
            | 
            -> contents                                                        
               | coverageCount : the number of hits registered in this cross bin
               0                                                               
            
Note that this only contains the elements which are relevant for merging!
"""
class UCIS_DB_Parser:
    def __init__(self):
        self.ucis_ns = 'ucis'
        self.ucis_ns_schema = 'http://www.w3.org/2001/XMLSchema-instance'
        # namespace map
        self.ns_map = {self.ucis_ns : self.ucis_ns_schema}
        # register the UCIS namespace
        ET.register_namespace(self.ucis_ns, self.ucis_ns_schema)
        self.ucis_db = {
            "instanceCoverages"  : '{0}:instanceCoverages' .format(self.ucis_ns),
            "covergroupCoverage" : '{0}:covergroupCoverage'.format(self.ucis_ns),
            "cgInstance"         : '{0}:cgInstance'        .format(self.ucis_ns),
            "coverpoint"         : '{0}:coverpoint'        .format(self.ucis_ns),
            "coverpointBin"      : '{0}:coverpointBin'     .format(self.ucis_ns),
            "range"              : '{0}:range'             .format(self.ucis_ns),
            "contents"           : '{0}:contents'          .format(self.ucis_ns),
            "cross"              : '{0}:cross'             .format(self.ucis_ns),
            "crossBin"           : '{0}:crossBin'          .format(self.ucis_ns),
            "crossExpr"          : '{0}:crossExpr'         .format(self.ucis_ns),
            "index"              : '{0}:index'             .format(self.ucis_ns),
            "userAttr"           : '{0}:userAttr'          .format(self.ucis_ns)
        }
        # the master ucis DB which will be "merged" into when parsing additional DBs
        self.mergeDBtree = None
        self.mergeDBroot = None
    
    def find_ucis_element(self, element, subElementName):
        return element.find('{0}:{1}'.format(self.ucis_ns, subElementName), self.ns_map)
    
    def findall_ucis_children(self, element, subElementName):
        return element.findall('{0}:{1}'.format(self.ucis_ns, subElementName), self.ns_map)
    
    # formats an XPath ElementTree query to search for a specified element name
    # and an optional attribute name together with a certain attribute value
    def format_et_query(self, elementName, attribName = None, attribValue = None):
        query = "{0}:{1}".format(self.ucis_ns, elementName)
        if attribName is not None and attribValue is not None:
            query += "[@{0}='{1}']".format(attribName, attribValue)
        return query
    
    # searches and returns the first match of the XPath query in the mergeDBtree
    def find_merge_element_by_query(self, xpath_query):
        return self.mergeDBtree.find(xpath_query, self.ns_map)
    