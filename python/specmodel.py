# -*- coding: utf-8 -*-
from functions import *

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

# Todo: How to include multiple occurances of one tag!?

RADIATIVETRANS_DICT={
    "Id":"@id",
    "LowerStateRef":"{"+NAMESPACE+"}LowerStateRef",
    "UpperStateRef":"{"+NAMESPACE+"}UpperStateRef",
    "FrequencyValue":"{"+NAMESPACE+"}EnergyWavelength/*[local-name()='Frequency']/*[local-name()='Value']",
    "FrequencyAccuracy":"{"+NAMESPACE+"}EnergyWavelength/*[local-name()='Frequency']/*[local-name()='Accuracy']",
    "TransitionProbabilityA":"{"+NAMESPACE+"}Probability/{"+NAMESPACE+"}TransitionProbabilityA/{"+NAMESPACE+"}Value",
    "Log10WeightedOscillatorStrength":"{"+NAMESPACE+"}Probability/{"+NAMESPACE+"}Log10WeightedOscillatorStrength/{"+NAMESPACE+"}Value",
    "Multipole":"{"+NAMESPACE+"}Probability/{"+NAMESPACE+"}Multipole",
    "SpeciesID":"{"+NAMESPACE+"}SpeciesRef",
    "ProcessClass":"{"+NAMESPACE+"}ProcessClass/{"+NAMESPACE+"}Code[]",
    }


STATES_DICT={
    "StateID":"get('stateID')",
    "SpecieID":"getparent().get('speciesID')",
    "InChIKey":"getparent().MolecularChemicalSpecies.InChIKey",    
    "StateEnergyValue":"MolecularStateCharacterisation.StateEnergy.Value",
    "StateEnergyUnit":"MolecularStateCharacterisation.StateEnergy.Value.get('units')",
    "StateEnergyOrigin":"MolecularStateCharacterisation.StateEnergy.get('energyOrigin')",
    "TotalStatisticalWeight":"MolecularStateCharacterisation.TotalStatisticalWeight",
    "NuclearSpinIsomerName":"MolecularStateCharacterisation.NuclearSpinIsomer.Name",
    "NuclearSpinIsomerLowestEnergy":"MolecularStateCharacterisation.NuclearSpinIsomer.get('lowestEnergyStateRef')",
    }


ATOMS_DICT={
    "SpeciesID":"Isotope.Ion.get('speciesID')",
    "ChemicalElementNuclearCharge":"ChemicalElement.NuclearCharge",
    "ChemicalElementSymbol":"ChemicalElement.ElementSymbol",
    "MassNumber":"Isotope.IsotopeParameters.MassNumber",
    "Mass":"Isotope.IsotopeParameters.Mass.Value",
    "MassUnit":"Isotope.IsotopeParameters.Mass.Value.get('units')",
    "IonCharge":"Isotope.Ion.IonCharge",
    "InChIKey":"Isotope.Ion.InChIKey",
    }

MOLECULES_DICT={
    "SpeciesID":"get('speciesID')",
    "ChemicalName":"MolecularChemicalSpecies.ChemicalName.Value",
    "Comment":"MolecularChemicalSpecies.Comment",
    "InChI":"MolecularChemicalSpecies.InChI",
    "InChIKey":"MolecularChemicalSpecies.InChIKey",
    "VAMDCSpeciesID":"MolecularChemicalSpecies.VAMDCSpeciesID",
    "ChemicalName":"MolecularChemicalSpecies.MoleculeStructure",
    "OrdinaryStructuralFormula":"MolecularChemicalSpecies.OrdinaryStructuralFormula.Value",
    "MolecularWeight":"MolecularChemicalSpecies.StableMolecularProperties.MolecularWeight.Value",
    "StoichiometricFormula":"MolecularChemicalSpecies.StoichiometricFormula",
    "PartitionFunction":"MolecularChemicalSpecies.PartitionFunction[]",
    }

PARTITIONFUNCTIONS_DICT={
    "SpeciesID":"getparent().getparent().get('speciesID')",
    "NuclearSpinIsomer":"NuclearSpinIsomer.Name",    
    "PartitionFunctionT":"T.DataList",    
    "PartitionFunctionQ":"Q.DataList",    
    "Comments":"Comments",
    }

COLLISIONALTRANS_DICT={

    "Id":"get('id')",
    "ProcessClassCode":"ProcessClass.Code",
    "Reactant":"Reactant[].SpeciesRef.text",
    "Product":"Product[].SpeciesRef.text",
#    "Reactant1":"Reactant[0].SpeciesRef.text",
#    "Reactant2":"Reactant[1].SpeciesRef.text",
#    "Product1":"Product[0].SpeciesRef.text",
#    "Product2":"Product[1].SpeciesRef.text",
    "DataDescription":"DataSets.DataSet.get('dataDescription')",
    "TabulatedData":"DataSets.DataSet.TabulatedData",
    "X":"DataSets.DataSet.TabulatedData.X.DataList",
    "XUnits":"DataSets.DataSet.TabulatedData.X.get('units')",
    "Y":"DataSets.DataSet.TabulatedData.Y.DataList",
    "YUnits":"DataSets.DataSet.TabulatedData.Y.get('units')",
    "FitParameters":"DataSets.DataSet.FitData",
    "Comment":"Comments",
    }


def isVibrationalStateLabel(label):
    """
    Checks if the label defines a vibrational state
    """
    if label[0]!='v':
        return False
    try:
        int(label[1])
        return True
    except IndexError:
        return True
    except ValueError:
        return False

def read_element(item):
    """
    """
    try:
        return eval(item)
    except:
        return None

def read_element2(item,path):
    """
    """
    print item, path
    try:
        return eval("item.path")
    except:
        return None

def convert_tabulateddata(item):
    """
    Converts an element of type {..xsams..}TabulatedData into a dictionary
    with elements from X as key and elements from Y as values

    Returns:

    datadict = (dictionary) with datapoints
    xunits = (string) unit of key elements
    yunits = (string) containing unit of value elements
    comment = (string)
    """
    
    x = item.X.DataList.text.split(" ")
    y = item.Y.DataList.text.split(" ")
    xunits = item.X.get('units')
    yunits = item.Y.get('units')
    comment = item.Comments.text
    
    datadict = {}
    for i in range(len(x)):
        datadict[x[i]]=y[i]

    return datadict, xunits, yunits, comment

def convert_partitionfunctions(item):
    """
    Converts an element of type {..xsams..}abulatedData into a dictionary
    with elements from X as key and elements from Y as values

    Returns:

    datadict = (dictionary) with datapoints
    xunits = (string) unit of key elements
    yunits = (string) containing unit of value elements
    comment = (string)
    """
    
    T = item.T.DataList.text.split(" ")
    Q = item.Q.DataList.text.split(" ")
    Tunits = item.T.get('units')
    try:
        nuclearSpinIsomer = item.NuclearSpinIsomer.Name.text
    except:
        nuclearSpinIsomer = ""
    try:
        comments = item.Comments.text
    except:
        comments = ""
    
    datadict = {}
    for i in range(len(T)):
        datadict[T[i]]=Q[i]

    return datadict, Tunits, comments, nuclearSpinIsomer


def convert_fitdata(item):
    """
    """
    parameters={}
    arguments={}
    function=None
    if item.__dict__.has_key('FitParameters'):

        function = item.FitParameters.get('functionRef')

        if item.FitParameters.__dict__.has_key('FitParameter'):
            num_parameters = item.FitParameters.FitParameter.__len__()
            
            for i in range(num_parameters):
                try:
                    name = item.FitParameters.FitParameter[i].get('name')
                except:
                    name = 'parameter%d' % i
                try:
                    units = eval("item.FitParameters.FitParameter[%d].Value.get('units')" % i)
                except:
                    units=''
                try:
                    method = eval("item.FitParameters.FitParameter[%d].get('methodRef')" % i)
                except:
                    method=''
                try:
                    value = eval("item.FitParameters.FitParameter[%d].Value.text" % i)
                except:
                    value=''
                try:
                    accuracy = eval('item.FitParameters.FitParameter[%d].Accuracy.text' % i)
                except:
                    accuracy = ''
                try:
                    comments = eval('item.FitParameters.FitParameter[%d].Comments.text' % i)
                except:
                    comments = ''
                try:
                    source = eval('item.FitParameters.FitParameter[%d].SourceRef.text' % i)
                except:
                    source = ''
                parameters[name]={'units':units, 'value':value, 'accuracy':accuracy, 'comments':comments, 'source':source}

        if item.FitParameters.__dict__.has_key('FitArgument'):
            num_arguments = item.FitParameters.FitArgument.__len__()
            for i in range(num_arguments):
                try:
                    name = eval("item.FitParameters.FitArgument[i].get('name')")
                except:
                    name = 'Argument%d' % i
                try:
                    units = eval("item.FitParameters.FitArgument[i].Value.get('units')")
                except:
                    units = ''
                try:
                    description = eval("item.FitParameters.FitArgument.Description.text")
                except:
                    description = ''
                try:
                    lowerlimit = eval("item.FitParameters.FitArgument.LowerLimit.text")
                except:
                    lowerlimit = ''
                try:
                    upperlimit = eval("item.FitParameters.FitArgument.UpperLimit.text")
                except:
                    upperlimit = ''
                    
                arguments[name]={'units':units, 'description':description, 'lowerlimit':lowerlimit,'upperlimit':upperlimit}

    return {'parameters':parameters, 'arguments':arguments, 'function':function}

class Atom(object):

    def __init__(self,xml):
        self.xml = xml
        
        if self.xml is not None:
            self.readXML(self.xml)

    def __repr__(self):
        return "%s %s %s %s" % (self.SpeciesID, self.ChemicalElementSymbol, self.ChemicalElementNuclearCharge, self.InChIKey)

    def additem(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass
        
    def readXML(self, xml):
        for el in ATOMS_DICT:
            try:
                item = eval("self.xml.%s" % ATOMS_DICT[el])
                self.additem(el, item )
            except:
                pass
            
        
class Molecule(object):

    def __init__(self, xml):
        self.xml = xml

        if self.xml is not None:
            self.readXML(self.xml)

    def __repr__(self):
        return "%s: %s, %s, %s, %s" % (self.SpeciesID, self.InChIKey, self.OrdinaryStructuralFormula, self.StoichiometricFormula, unicode(self.Comment))

    def additem2(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass
                
    def additem(self, item, value):
        try:
            if isiterable(value):
                value_list = []
                for row in value:
                    if hasattr(row,'tag') and row.tag=="{%s}PartitionFunction" % NAMESPACE:
                        pf_list, Tunits, comment, nsi = convert_partitionfunctions(row)
                        value_list.append({"Values":pf_list, "Unit": Tunits, "Comment":comment, "NuclearSpinIsomer":nsi})
                        
                        setattr(self, item, value_list)
                        #setattr(self, item+"TUnits",Tunits)
                        #setattr(self, item+"Comment",comment)
                    else:
                        setattr(self, item, row)
            else:
                setattr(self, item, value)
        except Exception, e:
            print "Error occured: %s" % e
        
    def readXML(self, xml):
        for el in MOLECULES_DICT:
            try:

                if MOLECULES_DICT[el].find("[]")>-1:
                    iterel = eval("self.xml.%s" % MOLECULES_DICT[el][0:MOLECULES_DICT[el].find("[]")])
                    num_elements = iterel.__len__()
                    item = []
                    for i in range(num_elements):
                        item.append( eval("self.xml.%s" % MOLECULES_DICT[el].replace("[]","["+str(i)+"]")) )

                else:             
                    item = eval("self.xml.%s" % MOLECULES_DICT[el])

                self.additem(el, item )
            except:
                pass


class Partitionfunctions(object):

    def __init__(self, xml):
        self.xml = xml

        if self.xml is not None:
            self.readXML(self.xml)

    def __repr__(self):
        return "%s: %s" % (self.SpeciesID, self.PartitionFunctionT)

        
    def additem(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass
        
    def readXML(self, xml):
        for el in PARTITIONFUNCTIONS_DICT:
            try:
                item = eval("self.xml.%s" % PARTITIONFUNCTIONS_DICT[el])
                self.additem(el, item )
            except:
                pass



class QuantumNumbers(object):
#    case = None
#    ns = None
#    xsamsstateel = None
    
    def getns(self):
        if not self.ns and self.case:
            self.ns = "{%s/cases/%s}" % (NAMESPACE, self.case)
            
        return self.ns
        
            
    def __init__(self, xsamsstateel):
        self.xsamsstateel = xsamsstateel
        self.qns = {}
        self.qn_string = ""
        self.ns = None
        self.case = None
        self.vibstate = ''
        
        self.case = xsamsstateel.Case.get('caseID')
        self.ns = self.getns()
        for i in xsamsstateel.Case.iterchildren():
            for j in i.iterchildren():
                label, value, attributes = self.parse_qn(j)
                self.qns[label]= value
                #self.qns[j.tag.replace(self.ns,"")] = j
                self.qn_string += "%s = %s; " % (str(label),str(value))

                if isVibrationalStateLabel(label) and int(value)!=0:
                    self.vibstate += "%s=%s, " % (str(label),str(value))
            # remove last ', ' from the string
            if self.vibstate == '':
                self.vibstate = 'v=0'
            else:
                self.vibstate = self.vibstate[:-2]
                

    def parse_qn(self, qn_element):
        """
        evaluates the quantum number element with its attributes
        """
        if len(self.ns)>0:
            label = qn_element.tag.replace(self.ns,"")
        else:
            label = qn_element.tag
        
        value = qn_element.text
        # loop through all the attributes
        attributes={}
        for item in  qn_element.items():
            if len(item)==2:
                attributes[item[0]]=item[1]
                if item[0]=='mode':
                    label = label.replace('i',item[1])
                    label = label.replace('j',item[1])
                elif item[0]=='j':
                    label = label.replace('j',item[1])
                elif item[0]=='i':
                    label = label.replace('i',item[1])
                elif item[0]=='nuclearSpinRef':
                    label="%s_%s" % (label, item[1])
            elif len(item)==1:
                attributes[item[0]]=None
            else:
                pass
    
        return label, value, attributes
    

    def __eq__(self,other):
        # Check if cases agree
        if self.case != other.case:
            return False
        # Check if the same quantum numbers are present in both descriptions
        #if self.qns.keys().sort() != other.qns.keys().sort():

        # check if quantum numbers agree;
        # Use 0, if vibrational state quantum numbers are not
        # explecitly defined, in one of the quantum number sets
        if len(self.qns)< len(other.qns):
            qns1=self.qns
            qns2=other.qns
        else:
            qns1=other.qns
            qns2=self.qns
            
        for qn in qns2:
            if qns1.has_key(qn):
                if qns1[qn]!=qns2[qn]:
                    return False
            else:
                if qn not in ['v','vi'] or int(qns2[qn])!=0:
                    return False
                      
        return True

    def __ne__(self,other):
        ## Check if cases agree
        #if self.case != other.case:
        #    return True
        ## Check if the same quantum numbers are present in both descriptions
        ##if self.qns.keys().sort() != other.qns.keys().sort():
        #if self.qns.keys()!= other.qns.keys():
        #    return True

        ## Loop through all the quantum numbers and check if they agree        
        #for qn in self.qns:
        #    if self.qns[qn]!=other.qns[qn]:
        #        return True
            
        #return False
        return not self.__eq__(other)


class Source(object):
#    xml = None

    def __init__(self, xml):
        self.xml = xml
        
    def getauthors(self):
        if self.xml is None:
            return ""
        authorlist=""
        for i in self.xml.Authors.Author:
            authorlist += "%s, " % i.Name

        return authorlist
        
    def getsourcestr(self):
        
        if self.xml is None:
            return ""
        string = self.getauthors()
        string += "%s, " % self.xml.SourceName
        string += "%s, " % self.xml.Volume
        string += "%s, " % self.xml.PageBegin
        string += "(%s)" % self.xml.Year

        return string


class RadiativeTransition(object):
#    xml = None


    def __init__(self, xml):
        self.xml=xml
        
        if self.xml is not None:
            self.readXML(self.xml)

    def additem(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass
        
    def readXML(self, xml):
        for el in RADIATIVETRANS_DICT:
            
            if RADIATIVETRANS_DICT[el].find("[]")>-1:
                #iterel = eval("self.xml.%s" % RADIATIVETRANS_DICT[el][0:RADIATIVETRANS_DICT[el].find("[]")])
                item = xml.findall(RADIATIVETRANS_DICT[el][:-2])
                #num_elements = iterel.__len__()
#                item = []
 #               for i in iterel:
  #                  item.append(i)
            else:            
                item=xml.find(RADIATIVETRANS_DICT[el])

            self.additem(el, item )
            # check for attributes
            try:
                for attribute in item.keys():
                    self.additem(el+attribute.capitalize(), item.get(attribute))
            except:
                pass
            
    def __repr__(self):
        return "%s: %s, %s, %s" % (self.Id, self.FrequencyValue, self.FrequencyAccuracy, self.TransitionProbabilityA)


class CollisionalTransition(object):

    def __init__(self, xml):
        self.xml=xml
        
        if self.xml is not None:
            self.readXML(self.xml)

    def additem(self, item, value):
        try:
            
            # Check for tabulated data
            if hasattr(value,'tag') and value.tag=="{%s}TabulatedData" % NAMESPACE:
                value,xunits, yunits, comment = convert_tabulateddata(value)
                setattr(self, item, value)
                setattr(self, item+"XUnits",xunits)
                setattr(self, item+"YUnits",yunits)
                setattr(self, item+"Comment",comment)
            # Check for fit data
            elif hasattr(value,'tag') and value.tag=="{%s}FitData" % NAMESPACE:
                fitdata = convert_fitdata(value)
                setattr(self, item, fitdata)
            else:
                setattr(self, item, value)
        except:
            pass


    def readXML(self, xml):
        """
        Appends attributes to this CollisionalTransition object.
        The attributes are defined in the dictionary COLLISIONALTRANS_DICT.
        Elements in the dictionary with values containing '[]' are assumed to be
        lists (multiple elements within the tag).
        """
        
        for el in COLLISIONALTRANS_DICT:
            try:
                if COLLISIONALTRANS_DICT[el].find("[]")>-1:
                    iterel = eval("self.xml.%s" % COLLISIONALTRANS_DICT[el][0:COLLISIONALTRANS_DICT[el].find("[]")])
                    num_elements = iterel.__len__()
                    item = []
                    for i in range(num_elements):
                        item.append( eval("self.xml.%s" % COLLISIONALTRANS_DICT[el].replace("[]","["+str(i)+"]")) )

                else:
                    item = eval("self.xml.%s" % COLLISIONALTRANS_DICT[el])
                    
                self.additem(el,item)
            except:
                pass
            

class State(object):
    """
    State object which provides state information. 
    """

    def __init__(self, xml):
        self.xml=xml
        
        if self.xml is not None:
            self.readXML(self.xml)

    def __repr__(self):
        return "%s %s %s %s" % (self.StateID, self.SpecieID, self.StateEnergyValue, self.StateEnergyUnit)

    def additem(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass
        
    def readXML(self, xml):
        for el in STATES_DICT:
            try:
                item = eval("self.xml.%s" % STATES_DICT[el])
                self.additem(el, item )
            except:
                pass
            
        # Attach Quantum numbers
        try:
            self.QuantumNumbers = QuantumNumbers(xml)
        except:
            pass


    def __eq__(self,other):

        # There should be also a check for specie's inchikey
        if self.InChIKey != other.InChIKey:
            return False
        # Check if quantum numbers agree
        if self.QuantumNumbers != other.QuantumNumbers:
            return False

            
        return True

    def __ne__(self,other):

        # There should be also a check for specie's inchikey
        if self.InChIKey != other.InChIKey:
            return True

        # Check if quantum numbers agree
        if self.QuantumNumbers != other.QuantumNumbers:
            return True

            
        return False
