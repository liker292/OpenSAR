
import xml.etree.ElementTree as ET

__all__ = ['Arxml','IsArxmlList']

def IsArxmlList(arxml):
    assert(isinstance(arxml, Arxml))
    try:
        max = arxml.descriptor.attrib['Max']
        return True
    except:
        return False
    
class Arxml():
    """
        For easy understanding and implementation, standard AUTOSAR Arxml rule is not adopted.
    More information about standard AUTOSAR Arxml, please see <AUTOSAR_ModelPersistenceRulesforXML.pdf>
    
        The rule of this version Arxml is defined by parai from the view of application and parai's 
    understanding of AUTOSAR.
    """
    version = 0.01 # initialize 
    def __init__(self,descriptor,configuration=None):
        # save input parameter
        assert(isinstance(descriptor, ET.Element))
        self.descriptor = descriptor
        self.tag  = self.descriptor.tag
        # Load configuration
        if(configuration != None):
            self.configuration = configuration
        # New configuration according to descriptor
        else:
            self.__newConfiguration()
    
    def __newConfiguration(self): # private
        self.configuration = ET.Element(self.descriptor.tag)
        for [key,type] in self.descriptor.items():
            self.configuration.attrib[key] = 'TBD'
    
    def getMaxChildAllowed(self):
        assert(IsArxmlList(self))
        
        return int(self.descriptor.attrib['Max'],10)

    def attrib(self,key,value=None):
        """ if value is none, return attrib, else set attrib"""
        isValidKey = False
        for [key1,type1] in self.descriptor.items():
            if(key == key1):
                isValidKey = True
                break
        if(isValidKey):
            if(value == None):
                return self.configuration.attrib[key]
            else:
                self.configuration.attrib[key] = str(value)
        else:
            if(IsArxmlList(self)==False):
                print 'Arxml: Error (key,value)=(%s,%s) for %s'%(key,value,self.descriptor.tag)
            if(value==None):
                return ''
    
    def __str__(self):
        cstr = '%s ['%(self.configuration.tag)
        for config in self.configuration:
            cstr += str(config)
        cstr += ']'
        return cstr

    def childArxmls(self):
        arxmls = []
        for descriptor in self.descriptor:
            tcfg  = None
            for configuration in self.configuration:
                if(configuration.tag == descriptor.tag):
                    tcfg = configuration
                    break
            arxmls.append(Arxml(descriptor,tcfg))
        return arxmls
    
    def childDescriptors(self):
        Descriptors = []
        for descriptor in self.descriptor:
            Descriptors.append(descriptor)
        return Descriptors