from enum import Enum
import numpy as np
import pandas as pd
import visa
import misc
from time import sleep
import re

#Class for operating the Keithley 2000

################################################
########## Created by James Patchett ###########
################################################
#### Please contact physics@jpatchett.co.uk ####
################################################


#Enum of allowed measured voltage ranges
class MEAS_V_RAN(Enum): 
    
    mV200 = 200e-3
    V2 = 2
    V20 =20
    V200 = 200
    
#Enum of allowed measurmented current ranges
class MEAS_I_RAN(Enum):
    uA1 = 1e-6
    uA10 = 10e-6
    uA100 = 100e-6
    mA1 = 1e-3
    mA10 = 10e-3
    mA100 = 100e-3
    A1 = 1

#Enum of measurement volt ranges with compliance limits
class MEAS_V_RAN_CP(Enum): 
    #Format = [Measurement range, maximum compliance value]
    
    mV200 = [200e-3, 210e-3]
    V2 = [2, 2.1]
    V20 =[20, 21]
    V200 =[200,210]

#Same but for currents
class MEAS_I_RAN_CP(Enum):
    uA1 = [1e-6, 1.05e-6] 
    uA10 = [10e-6, 10.5e-6]
    uA100 = [100e-6, 105e-6]
    mA1 = [1e-3, 1.05e-3]
    mA10 = [10e-3, 10.5e-3]
    mA100 = [100e-3, 105e-3]
    A1 = [1, 1.05]

class MEAS_TYPE(Enum):
    voltage = "VOLT"
    current = "CURR"

class SRC_TYPE(Enum):
    voltage = "VOLT"
    current = "CURR"

#Enums for the possible ranges of source ranges for voltage and current respectively
class SRC_V_RAN(Enum):
    mV200 = 200e-3
    V2 = 2
    V20 =20
    V200 = 200

class SRC_I_RAN(Enum):
    uA1 = 1e-6
    uA10 = 10e-6
    uA100 = 100e-6
    mA1 = 1e-3
    mA10 = 10e-3
    mA100 = 100e-3
    A1 = 1


class keithly:

    #####################
    #### Constructor ####
    #####################

    #address:GPIB address of the keithly
    #rm: resource manager
    def __init__(self, address, rm, reset = True):
        #Attempt to communicate with the Keithly
        try:
            self.address = address
            self.rm = rm
            self.keith = rm.open_resource(address)
        except: 
            print("Keithly could not be opened at that address")
            self.address = None
            self.rm = None

        #Re-set the Keithly
        if(reset is True):
            self.keith.write("*RST")

        #Intialise values
        self.__src_type = "VOLT"
        self.__meas_type = "CURR"
        self.__src_range = "a"
        self.__src_level = 0
        self.__meas_range = "d"
        self.__compl = "c"
        self.__output = False


    ####################################
    ####################################
    ## Basic functions for programming #
    ##### the Kiethly's parameters #####
    ####################################
    ####################################

    #Set the source type
    def source(self, source_type): 

        if isinstance(source_type, str): #Accepts "volt" or "curr"
            
            #Only interested in the first 4 letters
            source_type = source_type[:4].upper()
            try:
                self.keith.write(":SOURCE:FUNC "+source_type)
                self.keith.write(":SOUR:"+source_type+":MODE FIXED")
                self.__src_type = source_type
            except:
                print("Err in source(). \n Could not communicate with the Keithly or not a valid source type. \n Only accepts arguments VOLTage (0) or CURRent (1)")

        elif isinstance(source_type, int):
            
            if(source_type == 0):
                try:
                    self.keith.write(":SOURCE:FUNC VOLT")
                    self.keith.write(":SOUR:VOLT:MODE FIXED")

                    self.__src_type = SRC_TYPE.voltage.value
                except:
                    print("Err in source(). \n Could not communicate successfully with the Keithly")
            
            elif(source_type == 1):
                try:
                    self.keith.write(":SOURCE:FUNC CURR")
                    self.keith.write(":SOUR:CURR:MODE FIXED")

                    self.__src_type = SRC_TYPE.current.value
                except:
                    print("Err in source(). \n Could not communicate successfully with the Keithly")
            else:
                print("Not a valid input.\n Only accepts arguments VOLTage (0) or CURRent (1)")


    def measure(self, measure_type):
        
        if isinstance(measure_type, str): #Accepts "volt" or "curr"
            
            #Only interested in the first 4 letters
            measure_type = measure_type[:4].upper()

            try:
                self.keith.write(":SENS:FUNC \""+measure_type+"\"")
                self.__meas_type = measure_type
            except:
                print("Err in source(). \n Could not communicate with the Keithly or not a valid source type. \n Only accepts arguments VOLTage (0) or CURRent (1)")

        elif isinstance(measure_type, int):
            
            if(measure_type == 0):
                try:
                    self.keith.write(":SENS:FUNC \"VOLT\"")
                    self.__meas_type = MEAS_TYPE.voltage.value
                except:
                    print("Err in source(). \n Could not communicate successfully with the Keithly")
            
            elif(measure_type == 1):
                try:
                    self.keith.write(":SENS:FUNC \"CURR\"")
                    self.__meas_type = MEAS_TYPE.current.value
                except:
                    print("Err in source(). \n Could not communicate successfully with the Keithly")
            else:
                print("Not a valid input.\n Only accepts arguments VOLTage (0) or CURRent (1)")

    #Set the measurement range
    #Can take either an array, in which case it sets both the measurment range and the compliance
    #Or just a double, the it just sets the measurment range
    def measure_range(self, meas_range):
        
        #If the user passes a normal array or a float then just proceed straight to the methods
        if((isinstance(meas_range, list) or isinstance(meas_range, np.ndarray))):
           self.__measure_range_arr(meas_range)

        elif(isinstance(meas_range, float) or isinstance(meas_range, int)):
            self.__measure_range(meas_range)
        #If they pass an enum, then convert to the appropriate value, then recursively call the function again
        else:
            self.measure_range(meas_range.value)

    #Private functions to actyally change the measure rang
    def __measure_range_arr(self, meas_range):

        if(self.__src_type == SRC_TYPE.current.value):
            try:
                print(":SENS:VOLT:RANG "+str(meas_range[0]))
                self.keith.write(":SENS:VOLT:PROT "+str(meas_range[1]))
                self.keith.write(":SENS:VOLT:RANG "+str(meas_range[0]))

            except IndexError:
                print("Value out of bounds. \n Expected an array of values of the form [measurement range, compliance]")
            except:
                print("Setting the measurement (Voltage) range failed")
            
        elif(self.__src_type == SRC_TYPE.voltage.value):
            try:
                self.keith.write(":SENS:CURR:PROT "+str(meas_range[1]))
                self.keith.write(":SENS:CURR:RANG "+str(meas_range[0]))
                
            except IndexError:
                print("Value out of bounds. \n Expected an array of values of the form [measurement range, compliance]")
            except:
                print("Setting the measurement (Currant) range failed")
    
    def __measure_range(self, meas_range):
        if(self.__src_type == SRC_TYPE.current.value):
                try:
                    self.keith.write(":SENS:VOLT:RANG "+str(meas_range))
                except:
                    print("Setting the measurement (Voltage) range failed")
            
        elif(self.__src_type == SRC_TYPE.voltage.value):
            try:
                self.keith.write(":SENS:CURR:RANG "+str(meas_range))
            except:
                print("Setting the measurement (Currant) range failed")

    #Set the compliance
    def set_complianc(self, comp):

        self.keith.write(":SENS:CURR:PROT "+str(comp))

    #the source delay is the time between the output being turned on, and the measurmenet being taken
    def set_source_delay(self, SDM):
        #SDM = time in miliseconds or true/false for auto delays

        #set auto-delay on/off
        if(isinstance(SDM, bool)):
            if(SDM is True or SDM.upper() == "ON"): 
                try:
                    self.keith.write(":SOUR:DEL:AUTO ON") 
                except:
                    print("Could not set-auto delay")    
            elif(SDM is False or SDM.upper() == "OFF"):
                try:
                    self.keith.write(":SOUR:DEL:AUTO OFF")
                except:
                    print("Could not set-auto delay")    
        else:
            try:
                self.keith.write(":SOUR:DEL "+str(SDM/1000))
            except:
                print("Could not set delay to "+SDM+" ms")

    #Set the source range
    def src_range(self, src_range):

        try:
            #If they use the enums then attempt to get the float value
            if(isinstance(src_range, float) is False):
                src_range = src_range.value

            self.keith.write(":SOUR:"+self.__src_type+":RANG "+str(src_range))
            self.__src_range = src_range
        except:
            print("Setting the source range (" +self.__src_type+") failed")
    
    #Set the actual soruce value
    def src_level(self, level):
        try:
            self.keith.write(":SOUR:"+self.__src_type+":LEV "+str(level))
            self.__src_level = level
        except:
            print("Could not set the source level")

    #Tell the Keithly to produce output or not
    def set_output(self, output):
        try:
            if(output is True):
                self.keith.write(":OUTP ON")
                self.__ouput = output
            elif(output is False):
                self.keith.write(":OUTP OFF")
                self.__output = output
        except:
            print("Could not change the output value")

    #Set the auto-zero on or off
    def set_auto_zero(self, auto_zero):
        try:
            if(auto_zero is True):
                self.keith.write(":SYST:AZER: ON")

            elif(autozero is False):
                self.keith.write(":SYST:AZER: OFF")
        except:
            print("Could not change auto-zero")

    #Read the data and convert to a numpy array of floats
    def read_to_arr(self):

        try:
        
            result = self.keith.query(":READ?")
            search = re.findall(r'[+-]\d\.[\d]*E[+-]\d*', result)

            data = np.empty(len(search))

            for i, found in enumerate(search):

                data[i] = float(found)

            return data
        except:
            print("Could no read the device")
            return None
        


    #Read the data
    def read(self):
        try:
            return self.keith.query(":READ?")
        except:
            print("Could not read the device")


    #Generic write command
    #Don't use if possible as it won't update the parameters
    def write(self, command):

        try:
            self.keith.write(command)
        except:
            print("Not a valid command or could not communicate with Keithly")

    #Generic query command
    def query(self, command):
        try:
            return self.keith.query(str(command))
        except:
            print("Not a valid command or could not communicate with Keithly")

    #Update the obect's parameters
    def update_params(self):
        print("TODO")

    ###################################
    ############ Getters ##############
    ###################################

    def get_src_type(self):
        return self.__src_type
    
    def get_meas_type(self):
        return self.__meas_type

    def get_meas_range(self):
        return self.__measure_range

    def get_compl(self):
        return self.__compl

    def get_src_level(self):
        return self.__src_level
    
    def get_src_range(self):
        return self.__src_range

    def get_ouput(self):
        return self.__output

    ##################################
    ######## Sweep programming #######
    ##################################

    #Simple linear and logarithmic sweeps based on the pre-programmed
    #sweep functions in the Keithley
    def linear_sweep(self, start, stop, step, auto  = True, repeats = 1.0, delay = None, pandas = True):

        num = (int)((stop-start)/step +1)*repeats

        try:
            self.keith.write(":SENS:FUNC:CONC OFF")
            self.keith.write(":SOUR:"+self.__src_type+":START "+str(start))
            self.keith.write(":SOUR:"+self.__src_type+":STOP "+str(stop))
            self.keith.write(":SOUR:"+self.__src_type+":STEP " +str(step))

            self.keith.write(":SOUR:"+self.__src_type+":MODE SWE")

            if(auto is True):
                self.keith.write(":SOUR:SWE:RANG AUTO")

            self.keith.write(":SOUR:SWE:SPAC LIN")

            print(":TRIG:COUN "+str(num))
            self.keith.write(":TRIG:COUN "+str(num))

            if(delay != None):
                self.keith.write(":SOUR:DEL "+str(delay/1000))


            #Read the data
            self.set_output(True)
            result = self.read_to_arr()
            self.set_output(False)

            #Return a pandas data frame if true
            if pandas is True:

                voltage = result[::5]
                current = result[1::5]
                dF_result = pd.DataFrame(data = voltage, columns = ['Voltage'])
                dF_result['Current'] = current

                return  dF_result

            else:
                return result 
        
        except:
            print("Linear sweep failed")


    
