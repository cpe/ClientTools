# -*- coding: utf-8 -*-
import functions 
import numpy
#from specmodel import *

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

# some usefull functions
def split_datalist(datalist):
    """
    """
    return datalist.text.split(" ")

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
            except AttributeError:
                print "Could not evaluate %s" % el
                #pass

            # check for attributes
##            try:
##                for attribute in item.keys():
##                    self.additem(el+attribute.capitalize(), item.get(attribute))
##            except:
##                pass

                
def _construct_dictmodelclass(model_definitions, module):
    class _DictModel(dict):
        DICT = construct_model(model_definitions['Dictionary'])
        def __init__(self, xml):
            dict.__init__(self)
            self.xml = xml
            for item in eval("%s" % self.DICT[model_definitions['Name']]):
                element = module.__dict__[model_definitions['Type']](item)
                self[element.Id] = element
                             
    return _DictModel
        
def _construct_class(model_definitions, module = None):
    class _Model(Model):
        DICT = construct_model(model_definitions['Dictionary'])
           
        def __repr__(self):
            retval = ""
            for field in model_definitions['representation_fields']:
                try:
                    retval += "%s " % self.__dict__[field]
                except KeyError:
                    retval += "None "
            return retval
        
    if model_definitions.has_key('methods'):
        for method in model_definitions['methods']:
            setattr(_Model, method['name'], method['method'])

    return _Model

def register_models(DICT_MODELS, module):
    for model in DICT_MODELS['model_types']:
        print "Register Class %s in %s" % (model['Name'], module.__name__)
        #setattr(module, model['Name'], _construct_class(model, module))
        model_class = _construct_class(model)
        setattr(__import__(__name__), model['Name'], model_class )
        setattr(module, model['Name'], model_class )


    for model in DICT_MODELS['dict_types']:
        print "Register DictClass %s in %s" % (model['Name'], module.__name__)
        setattr(module, model['Name'], _construct_dictmodelclass(model, module))
        

def register_method(method):
    setattr(__import__(__name__), method.__name__, method)


#register_models(DICT_MODELS, module = __import__(__name__) )
