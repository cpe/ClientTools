# -*- coding: utf-8 -*-
import functions 
import numpy

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

def construct_model(dictionary):

    model = {}
    for field in dictionary:
        code = ""
        code_add = ""
        iterator_code = None
        
        if dictionary[field].find("\\")>-1:
            path_array, function = dictionary[field].split("\\")
            path_array = path_array.split(".")
        else:
            function = None
            path_array = dictionary[field].split(".")
            
        for tag in path_array:
            # is an attribute
            if tag[0] == '@':
                #if len(code)>0:
                #    code = "find('%s')." % code[:-1]
                code_add = "get('%s')" % (tag[1:],)
                # attribute can only at the last position
                break
            # xpath expression -> do not attach namespace
            elif tag[-2:] == '[]' and tag[0] in ['*','.','/']:
                iterator_code = "self.xml.findall('%s%s')" % (code, tag[:-2])
                code = ""
            elif tag[-2:] == '[]':
                iterator_code = "self.xml.findall('%s{%s}%s')" % (code, NAMESPACE, tag[:-2])
                code = ""
                # if another tag follows loop has to go on otherwise add text
#                if tag == path_array[-1]:
#                    code = "[el.text for el in %s]" % code
#                    break
#                else:
#                    list_code = code
#                    code = "el."
            elif tag[0] in ['*','.','/']:
                code += "%s/" % tag
            # regular element -> attach namespace
            else:
                code += "{%s}%s/" % (NAMESPACE, tag)
                # put path into find() if it is the last tag

#            if tag == path_array[-1]:
#                code = "self.xml.find('%s').text" % code[:-1]

        # create code to generate a list if there was an iterable element
        if iterator_code is not None:
            if len(code) == 0:
                if function is not None:
                    if function == 'self':
                        code = "[el for el in %s]" % (iterator_code)
                    else:    
                        code = "[%s(el) for el in %s]" % (function, iterator_code)
                elif len(code_add) == 0:
                    code = "[el.text for el in %s]" % (iterator_code)
                else:
                    code = "[el.%s for el in %s]" % (code_add, iterator_code)
            else:
                if function is not None:
                    if function == 'self':
                        code = "[el.%s for el in %s]" % (code[:-1], iterator_code)
                    else:
                        code = "[%s(el.%s) for el in %s]" % (function, code[:-1], iterator_code)
                elif len(code_add) == 0:
                    code = "[el.%stext for el in %s]" % (code, iterator_code)
                    
        else:
            if len(code) == 0:
                if function is not None:
                    if function == 'self':
                        code = "self.xml"
                    else:
                        code = "%s(self.xml)" % (function,)
                elif len(code_add) > 0:
                    code = "self.xml.%s" % (code_add,)
                else:
                    print "ERROR --------" 
            else:
                if function is not None:
                    if function == 'self':
                        code = "self.xml.find('%s')" % (code[:-1],)
                    else:
                        code = "%s(self.xml.find('%s'))" % (function, code[:-1],)
                elif len(code_add) > 0:
                    code = "self.xml.find('%s').%s" % (code[:-1], code_add,)
                else:
                    code = "self.xml.find('%s').text" % (code[:-1],)
#                code = "text"
#            code = "el.%s for el in %s" % (code, list_code)
        model[field] = code
    return model
                
MAIN_DICT = {
    "Atoms":"Species.Atoms.Atom[]\\self",
    "Molecules":"Species.Molecules.Molecule[]\\self",
    "RadiativeTransitions":"Processes.Radiative.RadiativeTransition[]\\self",
    "CollisionalTransitions":"Processes.Collisions.CollisionalTransition[]\\self",
    }

RADIATIVETRANS_DICT = {
    "Id":"@id",
    "LowerStateRef":"LowerStateRef",
    "UpperStateRef":"UpperStateRef",
    "FrequencyValue":"EnergyWavelength.Frequency.Value",
    "FrequencyAccuracy":"EnergyWavelength.Frequency.Accuracy",
    "TransitionProbabilityA":"Probability.TransitionProbabilityA.Value",
    "Log10WeightedOscillatorStrength":"Probability.Log10WeightedOscillatorStrength.Value",
    "Multipole":"Probability.Multipole",
    "SpeciesID":"SpeciesRef",
    "ProcessClass":"ProcessClass.Code[]",
    }


STATES_DICT = {
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
    "PartitionFunction":"MolecularChemicalSpecies.PartitionFunction[]\\convert_partitionfunctions",
    "States":"MolecularState[]\\State",
    }

PARTITIONFUNCTIONS_DICT = {
#    "SpeciesID":"getparent().getparent().get('speciesID')",
    "NuclearSpinIsomer":"NuclearSpinIsomer.Name",    
    "PartitionFunctionT":"T.DataList",    
    "PartitionFunctionQ":"Q.DataList",    
    "Units":"T.@units",
    "Comments":"Comments",
    }

COLLISIONALTRANS_DICT = {

    "Id":"@id",
    "ProcessClassCode":"ProcessClass.Code",
    "Reactant":"Reactant[].SpeciesRef",
    "Product":"Product[].SpeciesRef",
#    "Reactant1":"Reactant[0].SpeciesRef.text",
#    "Reactant2":"Reactant[1].SpeciesRef.text",
#    "Product1":"Product[0].SpeciesRef.text",
#    "Product2":"Product[1].SpeciesRef.text",
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
MAIN_MODEL = construct_model(MAIN_DICT)
ATOMS_MODEL = construct_model(ATOMS_DICT)
MOLECULES_MODEL = construct_model(MOLECULES_DICT)
STATES_MODEL = construct_model(STATES_DICT)
PARTITIONFUNCTIONS_MODEL = construct_model(PARTITIONFUNCTIONS_DICT)
COLLISIONALTRANS_MODEL = construct_model(COLLISIONALTRANS_DICT)
RADIATIVETRANS_MODEL = construct_model(RADIATIVETRANS_DICT)
QUANTUMNUMBERS_MODEL = construct_model(QUANTUMNUMBERS_DICT)

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
    T = eval('item.%s.split(" ")' % PARTITIONFUNCTIONS_MODEL['PartitionFunctionT'].replace('self.xml.',''))
    Q = eval('item.%s.split(" ")' % PARTITIONFUNCTIONS_MODEL['PartitionFunctionQ'].replace('self.xml.',''))
    Tunits = eval('item.%s' % PARTITIONFUNCTIONS_MODEL['Units'].replace('self.xml.',''))
    try:
        nuclearSpinIsomer = eval('item.%s' % PARTITIONFUNCTIONS_MODEL['NuclearSpinIsomer'].replace('self.xml.',''))
    except:
        nuclearSpinIsomer = ""
    try:
        comments = eval('item.%s' % PARTITIONFUNCTIONS_MODEL['Comments'].replace('self.xml.',''))
    except:
        comments = ""
    
    datadict = {}
    for i in range(len(T)):
        datadict[T[i]]=Q[i]

    return {"Values":datadict, "Unit": Tunits, "Comment":comments, "NuclearSpinIsomer":nuclearSpinIsomer}


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

class Model(object):

    def __init__(self, xml):
        self.xml = xml
        
        if self.xml is not None:
            self.readXML(self.xml)
    
    def additem(self, item, value):
        try:
            setattr(self, item, value)
        except:
            pass

    def readXML(self, xml):
        for el in self.DICT:
            try:
                item = eval("%s" % self.DICT[el])
                self.additem(el, item )
            except:
                pass

            # check for attributes
##            try:
##                for attribute in item.keys():
##                    self.additem(el+attribute.capitalize(), item.get(attribute))
##            except:
##                pass

DICT_MODELS = [
    {'Name':'Atom',
     'Dictionary':ATOMS_MODEL,
     'init_functions':None,
     'representation_fields':('SpeciesID', 'ChemicalElementSymbol', 'ChemicalElementNuclearCharge', 'InChIKey'),
     },
    {'Name':'Molecule',
     'Dictionary':MOLECULES_MODEL,
     'init_functions':None,
     'representation_fields':('SpeciesID', 'InChIKey', 'OrdinaryStructuralFormula', 'StoichiometricFormula', 'Comment'),
     },
    
    ]

def _construct_class(model_definitions):
    class _Model(Model):
        DICT = model_definitions['Dictionary']

        def __repr__(self):
            retval = ""
            for field in model_definitions['representation_fields']:
                try:
                    retval += "%s " % self.__dict__[field]
                except KeyError:
                    retval += "None "
            return retval
        
    return _Model

def register_models():
    for model in DICT_MODELS:
        print "Register Class %s in %s" % (model['Name'], __name__)
        setattr(__import__(__name__), model['Name'], _construct_class(model))

##class Atom(Model):
    
##    DICT = ATOMS_MODEL

##    def __repr__(self):
##        return "%s %s %s %s" % (self.SpeciesID, self.ChemicalElementSymbol, self.ChemicalElementNuclearCharge, self.InChIKey)

        
##class Molecule(Model):

##    DICT = MOLECULES_MODEL
    
##    def __repr__(self):
##        return "%s: %s, %s, %s, %s" % (self.SpeciesID, self.InChIKey, self.OrdinaryStructuralFormula, self.StoichiometricFormula, unicode(self.Comment))


class Partitionfunctions(Model):

    DICT = PARTITIONFUNCTIONS_MODEL
    def __repr__(self):
        return "%s: %s" % (self.SpeciesID, self.PartitionFunctionT)


class QuantumNumbers(Model):

    DICT = QUANTUMNUMBERS_MODEL

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


class RadiativeTransition(Model):

    DICT = RADIATIVETRANS_MODEL

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
            

class State(Model):
    """
    State object which provides state information. 
    """

    DICT = STATES_MODEL

    def __repr__(self):
#        return "%s %s %s %s" % (self.StateID, self.SpecieID, self.StateEnergyValue, self.StateEnergyUnit)
        return "%s %s %s" % (self.StateID, self.StateEnergyValue, self.StateEnergyUnit)

    def readXML(self, xml):
        Model.readXML(self, xml)
#        for el in self.DICT:
#            try:
#                item = eval("self.xml.%s" % self.DICT[el])
#                self.additem(el, item )
#            except:
#                pass
            
        # Attach Quantum numbers
#        try:
#            self.QuantumNumbers = QuantumNumbers(xml)
#        except:
#            pass


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



##################################################
# process xml-data
#-------------------------------------------------

class Atoms(dict):

    DICT = MAIN_MODEL

    def __init__(self, xml):
        dict.__init__(self)

        self.xml = xml
        for atom in eval("%s" % self.DICT['Atoms']):
            at = Atom(atom)
            self[at.SpeciesID]=at
                
class Molecules(dict):

    DICT = MAIN_MODEL
    
    def __init__(self, xml):
        dict.__init__(self)
        
        self.xml = xml
        
        for molecule in eval("%s" % self.DICT['Molecules']):
            mol = Molecule(molecule)
            self[mol.SpeciesID]=mol
            
class RadiativeTransitions(dict):

    DICT = MAIN_MODEL

    def __init__(self, xml):
        dict.__init__(self)
        self.xml = xml
        
        for radtrans in eval("%s" % self.DICT['RadiativeTransitions']):
            rt = RadiativeTransition(radtrans)
            self[rt.Id]=rt


def populate_models(xml, add_states=False):

    data = {}
    for item in MAIN_MODEL:
        try:
            data[item] = eval("%s(xml)" % item)
        except NameError:
            pass
    if add_states and 'States' not in data.keys():
        data['States'] = {}
        for SpeciesID in data['Molecules']:
            for state in data['Molecules'][SpeciesID].States:
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
        
