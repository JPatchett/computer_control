import visa
import Instruments.instrument as inst
import time
import matlab.engine

class kepco(inst.instrument):

    def __init__(self, address, engine, ide):

        super().__init__(address, None, ide) 

    
        #Open the KEPCO
        self.engine = engine #Remember to add the kepco folder to the engine's path!

        #Set-up the directory
        self.status['Set_curr'] = 0
        self.status['Meas_curr'] = 0
        self.status['Set_volt'] = 0
        self.status['Meas_volt'] = 0
        self.status['Curr_prot'] = 0
        self.status['On'] = 0
        self.status['SER'] = 0 # The standard event register value

        #Open the kepco connection
        self.engine.open_kepco(address, nargout = 0)

        #Reset the kepco
        self.reset()


    #Read the output from the source
    #0 for current, 1 for voltage
    #Use with caution, seems to randomly break it
    def read(self, type):
        result = float(self.engine.kepco_read(type))

        if(type == 0):
            self.status['Meas_curr'] = result
        elif(type == 1):
            self.status['Meas_volt'] = result

        return result

    #Resets the instrument to 0 voltage and minimum current
    def reset(self):

        self.engine.kepco_reset(nargout  = 0)

        self.status['Set_curr'] = 0
        self.status['Set_volt'] = 0
        self.status['On'] = 0

    ##SETTERS

    #Set the Kepco's output
    def set_output(self, curr, volt):
        #Change the set curr/volt
        self.status['Set_curr'] = curr
        self.status['Set_volt'] = volt

        #Send the instruction to the KEPCO
        self.engine.kepco_set_output(curr, volt, nargout = 0)

    #Turn the output on
    def set_on(self, on):

        self.engine.kepco_set_on(on, nargout = 0)

        if(on == 1):
            self.status['On'] = 1
        elif(on == 0):
            self.status['On'] = 0

    #Methods to set the current and voltage independently
    def set_curr(self, curr):
        self.status['Set_curr'] = curr
        self.engine.kepco_set_current(curr, nargout = 0)

    def set_volt(self, volt):
        self.status['Set_volt'] = volt
        self.engine.kepco_set_volt(volt, nargout = 0)

    ##GETTERS

    #Is the output on or off
    def query_on(self):
        self.status['On'] = self.engine.kepco_query_on()
        return self.status['On']


