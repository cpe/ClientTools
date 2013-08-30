# -*- coding: utf-8 -*-
import functions 
import numpy

from basemodel import *
#import basemodel

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

########################################################################
# Dictionaries for the Model-Layout
#
# These dictionaries contain the information which Classes are generated
# and which fields they have. The key / value pair is the fieldname and
# a path to the element in the XSAMS (XML) - Tree. Each child is connected
# to its parent by ".". Brackets "[]" indicate that there are multiple
# elements of the same type which have to be looped over. A function
# can be applied to an element. The function name has to be connected to
# the path by "\\".
#-------------------------------------------------------------------------

RADIATIVETRANS_DICT = {
    "Id":"@id",
    "LowerStateRef":"LowerStateRef",
    "UpperStateRef":"UpperStateRef",
    "FrequencyValue":"EnergyWavelength.Frequency.Value",
    "FrequencyAccuracy":"EnergyWavelength.Frequency.Accuracy",
    "TransitionProbabilityA":"Probability.TransitionProbabilityA.Value",
    "IdealisedIntensity":"Probability.IdealisedIntensity.Value",
    "Multipole":"Probability.Multipole",
    "SpeciesID":"SpeciesRef",
    "ProcessClass":"ProcessClass.Code[]",
    }

STATES_DICT = {
    "Id":"@stateID",
    "StateID":"@stateID",
#    "SpecieID":"getparent().get('speciesID')",
#    "InChIKey":"getparent().MolecularChemicalSpecies.InChIKey",    
    "StateEnergyValue":"MolecularStateCharacterisation.StateEnergy.Value",
    "StateEnergyUnit":"MolecularStateCharacterisation.StateEnergy.Value.@units",
    "StateEnergyOrigin":"MolecularStateCharacterisation.StateEnergy.@energyOrigin",
    "TotalStatisticalWeight":"MolecularStateCharacterisation.TotalStatisticalWeight",
    "NuclearSpinIsomerName":"MolecularStateCharacterisation.NuclearSpinIsomer.Name",
    "NuclearSpinIsomerLowestEnergy":"MolecularStateCharacterisation.NuclearSpinIsomer.@lowestEnergyStateRef",
    "QuantumNumbers":"Case\\QuantumNumbers",
    }

ATOMS_DICT = {
    "Id":"Isotope.Ion.@speciesID",
    "SpeciesID":"Isotope.Ion.@speciesID",
    "ChemicalElementNuclearCharge":"ChemicalElement.NuclearCharge",
    "ChemicalElementSymbol":"ChemicalElement.ElementSymbol",
    "MassNumber":"Isotope.IsotopeParameters.MassNumber",
    "Mass":"Isotope.IsotopeParameters.Mass.Value",
    "MassUnit":"Isotope.IsotopeParameters.Mass.Value.@units",
    "IonCharge":"Isotope.Ion.IonCharge",
    "InChIKey":"Isotope.Ion.InChIKey",
    }

MOLECULES_DICT = {
    "Id":"@speciesID",
    "SpeciesID":"@speciesID",
    "ChemicalName":"MolecularChemicalSpecies.ChemicalName.Value",
    "Comment":"MolecularChemicalSpecies.Comment",
    "InChI":"MolecularChemicalSpecies.InChI",
    "InChIKey":"MolecularChemicalSpecies.InChIKey",
    "VAMDCSpeciesID":"MolecularChemicalSpecies.VAMDCSpeciesID",
#    "ChemicalName":"findtext('{"+NAMESPACE+"}MolecularChemicalSpecies/{"+NAMESPACE+"}MoleculeStructure')",
    "OrdinaryStructuralFormula":"MolecularChemicalSpecies.OrdinaryStructuralFormula.Value",
    "MolecularWeight":"MolecularChemicalSpecies.StableMolecularProperties.MolecularWeight.Value",
    "StoichiometricFormula":"MolecularChemicalSpecies.StoichiometricFormula",
    "PartitionFunction":"MolecularChemicalSpecies.PartitionFunction[]\\Partitionfunctions",
    "States":"MolecularState[]\\State",
    }

PARTITIONFUNCTIONS_DICT = {
#    "SpeciesID":"getparent().getparent().get('speciesID')",
    "NuclearSpinIsomer":"NuclearSpinIsomer.Name",    
    "PartitionFunctionT":"T.DataList\\split_datalist",    
    "PartitionFunctionQ":"Q.DataList\\split_datalist",    
    "Units":"T.@units",
    "Comments":"Comments",
    }

COLLISIONALTRANS_DICT = {
    "Id":"@id",
    "ProcessClassCode":"ProcessClass.Code",
    "Reactant":"Reactant[].SpeciesRef",
    "Product":"Product[].SpeciesRef",
    "DataDescription":"DataSets.DataSet.@dataDescription",
    "TabulatedData":"DataSets.DataSet.TabulatedData",
    "X":"DataSets.DataSet.TabulatedData.X.DataList",
    "XUnits":"DataSets.DataSet.TabulatedData.X.@units",
    "Y":"DataSets.DataSet.TabulatedData.Y.DataList",
    "YUnits":"DataSets.DataSet.TabulatedData.Y.@units",
    "FitParameters":"DataSets.DataSet.FitData",
    "Comment":"Comments",
    }

QUANTUMNUMBERS_DICT = {
    "Case":"@caseID",
    "__qnelements__":"*.*[]\\self",
}

#########################################################################
# Functions for the models
#
# If additional methods have to be added to a (Model) class they have to be
# defined here.
#------------------------------------
def states__eq__(self, other):
    """
    Compare if a states equals another one. This method will be
    connected to the States-Class and is needed to compare two states
    """
    
    # There should be also a check for specie's inchikey
    if self.InChIKey != other.InChIKey:
        return False
    # Check if quantum numbers agree
    if self.QuantumNumbers != other.QuantumNumbers:
        return False
    
    return True

def states__ne__(self, other):
    """
    Compare if a states does not equal another one. This method will be
    connected to the States-Class and is needed to compare two states
    """
    # There should be also a check for specie's inchikey
    if self.InChIKey != other.InChIKey:
        return True

    # Check if quantum numbers agree
    if self.QuantumNumbers != other.QuantumNumbers:
        return True

    return False

def partitionfunction_init(self, xml):
    """
    Creates a dictionary of Partitionfunctions (PF / Temperature) pairs
    """
    Model.__init__(self, xml)
    self.values = {}
    for i in range(len(self.PartitionFunctionT)):
        self.values[self.PartitionFunctionT[i]]=self.PartitionFunctionQ[i]
        
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

#################################################################
# Dictionary to Control Generation of Model- and Dictionary -
# Classes
#----------------------------------------------------------------
DICT_MODELS = {
    'model_types':[
        {'Name':'Atom',
         'Dictionary':ATOMS_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'ChemicalElementSymbol', 'ChemicalElementNuclearCharge', 'InChIKey'),
         },
        {'Name':'Molecule',
         'Dictionary':MOLECULES_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'InChIKey', 'OrdinaryStructuralFormula', 'StoichiometricFormula', 'Comment'),
         },
        {'Name':'State',
         'Dictionary':STATES_DICT,
         'init_functions':None,
         'methods':[{'name':'__eq__',
                     'method':states__eq__},
                    {'name':'__ne__',
                     'method':states__ne__}
                    ],
         'representation_fields':('StateID', 'StateEnergyValue', 'StateEnergyUnit'),
         },
        {'Name':'Partitionfunctions',
         'Dictionary':PARTITIONFUNCTIONS_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'PartitionFunctionT'),
         'methods':[{'name':'__init__',
                     'method':partitionfunction_init},
                    ],
         },
        {'Name':'RadiativeTransition',
         'Dictionary':RADIATIVETRANS_DICT,
         'init_functions':None,
         'representation_fields':('Id', 'FrequencyValue', 'FrequencyAccuracy', 'TransitionProbabilityA'),
         },
        ],
    'dict_types':[
        {'Name':'Atoms',
         'Dictionary':{"Atoms":"Species.Atoms.Atom[]\\self"},
         'Type':'Atom'},
        {'Name':'Molecules',
         'Dictionary':{"Molecules":"Species.Molecules.Molecule[]\\self"},
         'Type':'Molecule'},
        {'Name':'RadiativeTransitions',
         'Dictionary':{"RadiativeTransitions":"Processes.Radiative.RadiativeTransition[]\\self"},
         'Type':'RadiativeTransition'},
        ]
    }

register_models(DICT_MODELS, module = __import__(__name__) )

class QuantumNumbers(Model):

    DICT = construct_model(QUANTUMNUMBERS_DICT) #MODEL

    ns = None
    qn_string = ""
    vibstate = ""
    
    def __init__(self, xml):
        Model.__init__(self, xml)

        self.getns()
        
        # replace list of quantum numbers by dictionary
        self.qn_dict = {}
        for qn in self.__qnelements__:
            label, value, attributes = self.parse_qn(qn)
            self.qn_dict[label]= value
            #self.qns[j.tag.replace(self.ns,"")] = j
            self.qn_string += "%s = %s; " % (str(label),str(value))

            if isVibrationalStateLabel(label) and int(value)!=0:
                self.vibstate += "%s=%s, " % (str(label),str(value))
            # remove last ', ' from the string
        if self.vibstate == '':
            self.vibstate = 'v=0'
        else:
            self.vibstate = self.vibstate[:-2]

                
    def getns(self):
        if not self.ns:
            try:
                self.ns = "{%s/cases/%s}" % (NAMESPACE, self.Case)
            except:
                self.ns = ""
                
    
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
        if self.Case != other.Case:
            return False
        # Check if the same quantum numbers are present in both descriptions
        #if self.qns.keys().sort() != other.qns.keys().sort():

        # check if quantum numbers agree;
        # Use 0, if vibrational state quantum numbers are not
        # explecitly defined, in one of the quantum number sets
        if len(self.qn_dict)< len(other.qn_dict):
            qns1=self.qn_dict
            qns2=other.qn_dict
        else:
            qns1=other.qn_dict
            qns2=self.qn_dict

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

register_method(QuantumNumbers)

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
            

##################################################
# process xml-data
#-------------------------------------------------

def populate_models(xml, add_states=False):
    data = {}
    for item in DICT_MODELS['dict_types']:
        try:
            data[item['Name']] = eval("%s(xml)" % item['Name'])
        except NameError:
            pass
    if add_states and 'States' not in data.keys():
        data['States'] = {}
        for SpeciesID in data['Molecules']:
            for state in data['Molecules'][SpeciesID].States:
                state.SpeciesID = SpeciesID
                data['States'][state.StateID] = state
            
    return data
    
    
def calculate_partitionfunction(states, temperature = 300.0):

    pfs = {}
    distinct_list = {}
    # create a distinct list of states
    for state in states:
        id = states[state].SpecieID
        qn_string = states[state].QuantumNumbers.qn_string
        
        if not id in distinct_list:
            distinct_list[id] = {}
        distinct_list[id][qn_string] = states[state]

    for specie in distinct_list:
        pfs[specie] = 0
        for state in distinct_list[specie]:
            pfs[specie] += int(distinct_list[specie][state].TotalStatisticalWeight) * numpy.exp(-1.43878*distinct_list[specie][state].StateEnergyValue/temperature)
            

    return pfs
        
