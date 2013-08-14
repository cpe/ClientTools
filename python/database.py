# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from dateutil import parser

from functions import *
from query import *
from results import *

DATABASE_FILE = "cdms_sqlite.db"

class Database(object):

    def __init__(self):
        """
        Connect to database.

        Database will be created if it does not exist 
        """
        try:
            self.conn = sqlite3.connect(DATABASE_FILE)
        except sqlite3.Error, e:
            print " "
            print "Can not connect to sqlite3 databse %s." % DATABASE_FILE
            print "Error: %d: %s" % (e.args[0], e.args[1])
        return
        
    def create_structure(self):        
        """
        Create tables in the sqlite3 database

        Tables which will be created:
        - Partitionfunctions
        - Transitions
        """

        cursor = self.conn.cursor()
        #----------------------------------------------------------
        # drop tables if they exist
        stmts = ("DROP TABLE IF EXISTS Partitionfunctions;",
                 "DROP TABLE IF EXISTS Transitions;",)

        for stmt in stmts:
            cursor.execute(stmt)
        #----------------------------------------------------------


        #-------------------------------------------------
        # INSERT TRANSITIONS
    
        sql_create_transitions = """CREATE TABLE Transitions (
        T_Name TEXT,        
        T_Frequency REAL,
        T_Intensity REAL,
        T_EinsteinA REAL,
        T_Uncertainty REAL,
        T_EnergyLower REAL,
        T_UpperStateDegeneracy INTEGER,
        T_NuclearSpinIsomer TEXT,
        T_HFS TEXT,
        T_Case TEXT,
        T_UpperStateQuantumNumbers TEXT,
        T_LowerStateQuantumNumbers TEXT) """


        sql_create_partitionfunctions = """ CREATE TABLE Partitionfunctions (
        PF_Name TEXT,
        PF_VamdcSpeciesID TEXT,
        PF_SpeciesID TEXT,
        PF_NuclearSpinIsomer TEXT,
        PF_HFS TEXT,
        PF_1_072 REAL,
        PF_1_148 REAL,
        PF_1_230 REAL,
        PF_1_318 REAL,
        PF_1_413 REAL,
        PF_1_514 REAL,
        PF_1_622 REAL,
        PF_1_738 REAL,
        PF_1_862 REAL,
        PF_1_995 REAL,
        PF_2_138 REAL,
        PF_2_291 REAL,
        PF_2_455 REAL,
        PF_2_630 REAL,
        PF_2_725 REAL,
        PF_2_818 REAL,
        PF_3_020 REAL,
        PF_3_236 REAL,
        PF_3_467 REAL,
        PF_3_715 REAL,
        PF_3_981 REAL,
        PF_4_266 REAL,
        PF_4_571 REAL,
        PF_4_898 REAL,
        PF_5_000 REAL,
        PF_5_248 REAL,
        PF_5_623 REAL,
        PF_6_026 REAL,
        PF_6_457 REAL,
        PF_6_918 REAL,
        PF_7_413 REAL,
        PF_7_943 REAL,
        PF_8_511 REAL,
        PF_9_120 REAL,
        PF_9_375 REAL,
        PF_9_772 REAL,
        PF_10_471 REAL,
        PF_11_220 REAL,
        PF_12_023 REAL,
        PF_12_882 REAL,
        PF_13_804 REAL,
        PF_14_791 REAL,
        PF_15_849 REAL,
        PF_16_982 REAL,
        PF_18_197 REAL,
        PF_18_750 REAL,
        PF_19_498 REAL,
        PF_20_893 REAL,
        PF_22_387 REAL,
        PF_23_988 REAL,
        PF_25_704 REAL,
        PF_27_542 REAL,
        PF_29_512 REAL,
        PF_31_623 REAL,
        PF_33_884 REAL,
        PF_36_308 REAL,
        PF_37_500 REAL,
        PF_38_905 REAL,
        PF_41_687 REAL,
        PF_44_668 REAL,
        PF_47_863 REAL,
        PF_51_286 REAL,
        PF_54_954 REAL,
        PF_58_884 REAL,
        PF_63_096 REAL,
        PF_67_608 REAL,
        PF_72_444 REAL,
        PF_75_000 REAL,
        PF_77_625 REAL,
        PF_83_176 REAL,
        PF_89_125 REAL,
        PF_95_499 REAL,
        PF_102_329 REAL,
        PF_109_648 REAL,
        PF_117_490 REAL,
        PF_125_893 REAL,
        PF_134_896 REAL,
        PF_144_544 REAL,
        PF_150_000 REAL,
        PF_154_882 REAL,
        PF_165_959 REAL,
        PF_177_828 REAL,
        PF_190_546 REAL,
        PF_204_174 REAL,
        PF_218_776 REAL,
        PF_225_000 REAL,
        PF_234_423 REAL,
        PF_251_189 REAL,
        PF_269_153 REAL,
        PF_288_403 REAL,
        PF_300_000 REAL,
        PF_309_030 REAL,
        PF_331_131 REAL,
        PF_354_813 REAL,
        PF_380_189 REAL,
        PF_407_380 REAL,
        PF_436_516 REAL,
        PF_467_735 REAL,
        PF_500_000 REAL,
        PF_501_187 REAL,
        PF_537_032 REAL,
        PF_575_440 REAL,
        PF_616_595 REAL,
        PF_660_693 REAL,
        PF_707_946 REAL,
        PF_758_578 REAL,
        PF_812_831 REAL,
        PF_870_964 REAL,
        PF_933_254 REAL,
        PF_1000_000 REAL,
        PF_ResourceID TEXT,
        PF_URL TEXT,
        PF_Comment TEXT,
        PF_Timestamp)"""
    
        cursor.execute(sql_create_transitions)    
        cursor.execute(sql_create_partitionfunctions)

        #-------------------------------------------------------------
        
        return

    def insert_specie(self, Molecules=None, Atoms=None, node = None):
        """
        Insert species data into database

        data is stored in Partitionfunctions-table
        """
        cursor = self.conn.cursor()
        cursor.execute('BEGIN TRANSACTION')

        if node:
            resourceID = node.identifier
            url = node.url
        else:
            resourceID = 'NULL'
            url = 'NULL'
        
        # Insert molecules
        for id in Molecules:
            
            # Insert row in partitionfunctions
            try:
                cursor.execute("INSERT INTO Partitionfunctions (PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Comment, PF_ResourceID, PF_URL, PF_Timestamp) VALUES (?,?,?,?,?,?,?)",
                               ("%s" % (Molecules[id].OrdinaryStructuralFormula),
                                id,
                                "%s" % (Molecules[id].VAMDCSpeciesID),
                                "%s" % (Molecules[id].Comment),
                                resourceID,
                                "%s%s%s" % (url,"sync?LANG=VSS2&amp;REQUEST=doQuery&amp;FORMAT=XSAMS&amp;QUERY=Select+*+where+MoleculeSpeciesID%3D",id),
                                datetime.now()))
            except sqlite3.Error as e:
                print "An error occurred:", e.args[0]



            # Update Partitionfunctions
            try:
                for pfs in Molecules[id].PartitionFunction:
                    if not pfs['NuclearSpinIsomer']:
                        for temperature in pfs['Values']:
                        
                            try:
                                field = ("PF_%.3lf" % float(temperature)).replace('.','_')
                                sql = "UPDATE Partitionfunctions SET %s=? WHERE PF_SpeciesID=?" % field
                                cursor.execute(sql,(pfs['Values'][temperature],id))
                            except Exception, e:
                                print "SQL-Error: %s " % sql
                                print pfs['Values'][temperature],id
                                print "Error: %d: %s" % (e.args[0], e.args[1])
            except:
                pass


        self.conn.commit()
        cursor.close()
        return
    
        #except Exception, e:
        #        print Molecules[id].InChIKey[0]
        #        print "INSERT INTO Partitionfunctions (PF_Name, PF_SpeciesID, PF_Inchikey) VALUES (%s,%s,%s)" %  (Molecules[id].Comment[0],
#                                                                                                                  id,
#                                                                                                                  Molecules[id].InChIKey[0])

    def insert_radiativetransitions(self, species, node):
        """
        """
        # will contain a list of names which belong to one specie
        species_names = {}
        
        #----------------------------------------------------------
        # Create a list of species for which transitions will be
        # retrieved and inserted in the database.
        # Species have to be in the Partitionfunctions - table
        
        if not isiterable(species):
            species = [species]

        species_list = []
               
        cursor = self.conn.cursor()
        for specie in species:
            cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_HFS FROM Partitionfunctions WHERE PF_SpeciesID=? or PF_VamdcSpeciesID=?",
                           (specie, specie))
            rows = cursor.fetchall()
            for row in rows:
                species_list.append([row[0], row[1], row[2], row[3]])

        #--------------------------------------------------------------
        


        for specie in species_list:
            num_transitions = {}

            #------------------------------------
            # Retrieve data from the database
            
            id = specie[1]
            vamdcspeciesid = specie[2]
            hfs = specie[3]
            name = specie[0]
            # name should be formated like 'formula; state-info; hfs-info'
            name_array = name.split(';')

            formula = name_array[0].strip()
            try:
                stateInfo = name_array[1].strip()
            except:
                stateInfo = ''
                
            # get hfs-flag from the name. 
            try:
                hfsInfo = name_array[2].strip()
            except:
                hfsInfo = ''

            # Create query string
            query_string = "SELECT ALL WHERE VAMDCSpeciesID='%s'" % vamdcspeciesid            
            if hfs is not None and hfs.strip()!='':
                query_string += " and RadTransCode='%s'" % hfs
            query = Query()
            result = Result()
            
            # Get data from the database
            query.set_query(query_string)
            query.set_node(node)
        
            result.set_query(query)
            result.do_query()
            result.populate_model()
            #---------------------------------------

            
            cursor = self.conn.cursor()
            cursor.execute('BEGIN TRANSACTION')

            cursor.execute("DELETE FROM Transitions WHERE T_Name = ?", (name,))

        
            for trans in result.RadiativeTransitions:
                # data might contain transitions for other species (if query is based on ichikey/vamdcspeciesid).
                # Insert transitions only if they belong to the correct specie

                if result.RadiativeTransitions[trans].SpeciesID == id:
                    
                    # Get upper and lower state from the states table
                    upper_state = result.States["%s" % result.RadiativeTransitions[trans].UpperStateRef]                
                    lower_state = result.States["%s" % result.RadiativeTransitions[trans].LowerStateRef]
                   
                    # Get string which identifies the vibrational states involved in the transition
                    try:
                        if upper_state.QuantumNumbers.vibstate==lower_state.QuantumNumbers.vibstate:
                            t_state = str(upper_state.QuantumNumbers.vibstate).strip()
                        else:
                            #vup = upper_state.QuantumNumbers.vibstate.split(",")
                            #vlow = lower_state.QuantumNumbers.vibstate.split(",")
                            v_dict={}
                            for label in list(set(upper_state.QuantumNumbers.qns.keys()+lower_state.QuantumNumbers.qns.keys())):
                                if isVibrationalStateLabel(label):
                                    try:
                                        value_up=upper_state.QuantumNumbers.qns[label]
                                    except:
                                        value_up = 0
                                    try:
                                        value_low=lower_state.QuantumNumbers.qns[label]
                                    except:
                                        value_low = 0
                                    v_dict[label]=[value_up, value_low]
                            v_string = ''
                            valup_string = ''
                            vallow_string = ''
                            for v in v_dict:
                                v_string += "%s," % v
                                valup_string += "%s," % v_dict[v][0]
                                vallow_string += "%s," % v_dict[v][1]
                            if len(v_dict)>1:
                                t_state = "(%s)=(%s)-(%s)" % (v_string[:-1],valup_string[:-1],vallow_string[:-1])
                            else:
                                t_state = "%s=%s-%s" % (v_string[:-1],valup_string[:-1],vallow_string[:-1])

                            #t_state = '(%s)-(%s)' % (upper_state.QuantumNumbers.vibstate,lower_state.QuantumNumbers.vibstate)
                    except:
                        t_state = ''

                    # go to the next transition if state does not match
                    if t_state!=stateInfo and stateInfo is not None and stateInfo!='':
                        continue

                    # Get hyperfinestructure info if hfsInfo is None
                    # only then the hfsInfo has not been inserted in the species name
                    # (there can be multiple values in the complete dataset
                    if hfsInfo == '':
                        t_hfs = ''
                        try:
                            for pc in result.RadiativeTransitions[trans].ProcessClass:
                                if str(pc)[:3]=='hyp':
                                    t_hfs = str(pc)
                        except Exception, e:
                            print "Error: %s", e
                    else:
                        t_hfs = hfsInfo

                    # if hfs is not None and empty then only Transitions without hfs-flag
                    # should be processed
                    if hfs is not None and hfs!=t_hfs:
                        continue
                    
                    t_name = "%s; %s; %s" % (formula, t_state, t_hfs)
                    t_name = t_name.strip()
                    # update list of distinct species names.
                    if species_names.has_key(id):
                        if not t_name in species_names[id]:
                            species_names[id].append(t_name)
                            num_transitions[t_name]=0
                    else:
                        species_names[id]=[t_name]
                        num_transitions[t_name]=0

                    frequency = result.RadiativeTransitions[trans].FrequencyValue
                    uncertainty = "%lf" % result.RadiativeTransitions[trans].FrequencyAccuracy

                    # Get statistical weight if present
                    if upper_state.TotalStatisticalWeight:
                        weight = int(upper_state.TotalStatisticalWeight)
                    else:
                        weight = None

                    # Get nuclear spin isomer (ortho/para) if present 
                    try:
                        nsiName = upper_state.NuclearSpinIsomerName
                    except AttributeError:
                        nsiName = None

                    # Insert transition into database
                    try:
                        cursor.execute("""INSERT INTO Transitions (
                        T_Name,
                        T_Frequency,
                        T_EinsteinA,
                        T_Uncertainty,
                        T_EnergyLower, 
                        T_UpperStateDegeneracy,
                        T_HFS,
                        T_UpperStateQuantumNumbers,
                        T_LowerStateQuantumNumbers) VALUES
                        (?, ?,?,?,?, ?,?, ?,?)""",
                                       (t_name, 
                                        "%lf" % frequency,
                                        "%lf" %  result.RadiativeTransitions[trans].TransitionProbabilityA, 
                                        uncertainty, "%lf" % lower_state.StateEnergyValue, 
                                        weight,
                                        #upper_state.QuantumNumbers.case,
                                        t_hfs,
                                        str(upper_state.QuantumNumbers.qn_string),
                                        str(lower_state.QuantumNumbers.qn_string),                            
                                        ))
                        num_transitions[t_name]+=1
                    except Exception, e:
                        print "Transition has not been inserted:\n Error: %s" % e

            print "Processed: %s - %s" % (id,name)
            for row in num_transitions:
                print "      for %s inserted %d transitions" % (row, num_transitions[row])
            self.conn.commit()
            cursor.close()

        self.update_species_names(species_names)
        return num_transitions



    def dublicate_partitionfunctions(self, speciesid, name):

        sql_dublicate = """ INSERT INTO Partitionfunctions SELECT
        ?,
        PF_VamdcSpeciesID,
        PF_SpeciesID,
        PF_NuclearSpinIsomer,
        ?,
        PF_1_072,
        PF_1_148,
        PF_1_230,
        PF_1_318,
        PF_1_413,
        PF_1_514,
        PF_1_622,
        PF_1_738,
        PF_1_862,
        PF_1_995,
        PF_2_138,
        PF_2_291,
        PF_2_455,
        PF_2_630,
        PF_2_725,
        PF_2_818,
        PF_3_020,
        PF_3_236,
        PF_3_467,
        PF_3_715,
        PF_3_981,
        PF_4_266,
        PF_4_571,
        PF_4_898,
        PF_5_000,
        PF_5_248,
        PF_5_623,
        PF_6_026,
        PF_6_457,
        PF_6_918,
        PF_7_413,
        PF_7_943,
        PF_8_511,
        PF_9_120,
        PF_9_375,
        PF_9_772,
        PF_10_471,
        PF_11_220,
        PF_12_023,
        PF_12_882,
        PF_13_804,
        PF_14_791,
        PF_15_849,
        PF_16_982,
        PF_18_197,
        PF_18_750,
        PF_19_498,
        PF_20_893,
        PF_22_387,
        PF_23_988,
        PF_25_704,
        PF_27_542,
        PF_29_512,
        PF_31_623,
        PF_33_884,
        PF_36_308,
        PF_37_500,
        PF_38_905,
        PF_41_687,
        PF_44_668,
        PF_47_863,
        PF_51_286,
        PF_54_954,
        PF_58_884,
        PF_63_096,
        PF_67_608,
        PF_72_444,
        PF_75_000,
        PF_77_625,
        PF_83_176,
        PF_89_125,
        PF_95_499,
        PF_102_329,
        PF_109_648,
        PF_117_490,
        PF_125_893,
        PF_134_896,
        PF_144_544,
        PF_150_000,
        PF_154_882,
        PF_165_959,
        PF_177_828,
        PF_190_546,
        PF_204_174,
        PF_218_776,
        PF_225_000,
        PF_234_423,
        PF_251_189,
        PF_269_153,
        PF_288_403,
        PF_300_000,
        PF_309_030,
        PF_331_131,
        PF_354_813,
        PF_380_189,
        PF_407_380,
        PF_436_516,
        PF_467_735,
        PF_500_000,
        PF_501_187,
        PF_537_032,
        PF_575_440,
        PF_616_595,
        PF_660_693,
        PF_707_946,
        PF_758_578,
        PF_812_831,
        PF_870_964,
        PF_933_254,
        PF_1000_000,
        PF_ResourceID,
        PF_URL,
        PF_Comment,
        datetime('now')
        from Partitionfunctions WHERE PF_SpeciesID=? LIMIT 1"""

        try:
            hfs = name.split("; ")[2].strip()
        except:
            hfs = ''

        cursor = self.conn.cursor()
        cursor.execute(sql_dublicate, (name, hfs, speciesid))
        print "Created %s in Partitionfunctions" % str(name)
        self.conn.commit()
        cursor.close()
        

    def update_species_names(self, species_names):
        """
        """

        cursor = self.conn.cursor()
        # loop over list of species-Ids:
        for speciesid in species_names:
            delete_rows=[]
            
            cursor.execute("SELECT PF_Name, PF_HFS FROM Partitionfunctions WHERE PF_SpeciesID=?", [(speciesid)])
            rows = cursor.fetchall()
            num_rows = len(rows)
            # delete name from list, if name is already in the database.
            # if name is not in list, store name for later deletion
            for row in rows:
                try:
                    species_names[speciesid].remove(row[0].strip())
                except ValueError:
                    delete_rows.append(row[0])

            # Dublicate row for all the remaining names
            for name in species_names[speciesid]:
                self.dublicate_partitionfunctions(speciesid, name)

            # Delete rows which have been marked for deletion
            for name in delete_rows:
                cursor.execute("DELETE FROM Partitionfunctions WHERE PF_Name=?", (str(name),))
                print "Removed %s from Partitionfunctions" % str(name)

        self.conn.commit()
        cursor.close()
        
    def check_for_updates(self, node):
        """
        """

        count_updates = 0
        counter = 0
        #species_list = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, datetime(PF_Timestamp) FROM Partitionfunctions ")
        rows = cursor.fetchall()
        num_rows = len(rows)
        query = Query()
        result = Result()

        for row in rows:
            counter += 1
            print "%5d/%5d: Check specie %-55s (%-15s): " % (counter,num_rows, row[0],row[1]),
            #id = row[1]
            vamdcspeciesid = row[2]
#            query_string = "SELECT ALL WHERE VAMDCSpeciesID='%s'" % vamdcspeciesid
            query_string = "SELECT ALL WHERE SpeciesID=%s" % row[1][6:]
            query.set_query(query_string)
            query.set_node(node)
            
            result.set_query(query)
            try:
                changedate = result.getChangeDate()
            except:
                changedate = None
                
            tstamp = parser.parse(row[3]+" GMT")
            if changedate is None:
                print " -- UNKNOWN (Could not retrieve information)"
                continue
            if tstamp<changedate:
                print " -- UPDATE AVAILABLE " 
                count_updates += 1
            else:
                print " -- up to date"

        if count_updates == 0:
            print "\r No updates for your entries available"
        print "Done"


    def check_for_new_species(self, node):
        """
        """

        counter = 0
        cursor = self.conn.cursor()

        node.get_species()
        for id in node.Molecules:
            try:
                cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Timestamp FROM Partitionfunctions WHERE PF_SpeciesID=?", [(id)])
                exist = cursor.fetchone()
                if exist is None:
                    print "ID: %s" % node.Molecules[id]
                    counter += 1
            except Exception, e:
                print e
                print id
        print "There are %d new species available" % counter
            
        
    def showSpecies(self):

        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Timestamp FROM Partitionfunctions")
        rows = cursor.fetchall()
        for row in rows:
            print "%-10s %-60s %20s %s" % (row[1],row[0],row[2],row[3])

        
