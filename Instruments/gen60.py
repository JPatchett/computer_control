import visa
import Instruments.instrument as inst
import time

class gen60(inst.instrument):

    def __init__(self, address, rm, ide, resistance = 3):
        
        #Open up the resource
        super().__init__(address, rm, ide, rm_args = dict(read_termination = '\r', write_termination = '\r'))
        

        #Required to begin communication
        self.instrument.write("ADR 6")
        self.instrument.read()

        #Now can begin communicating

        #Set the resistance of the coil
        self.status['Resistance'] = resistance

    ## Setters
 
    # Reset function
    def reset(self):
        self.instrument.write("RST")

    # Set the output voltage
    def set_output_volt(self, voltage):
        self.instrument.write("PV "+str(voltage))
    
    # Set the output current
    def set_output_curr(self, current):
        self.instrument.write("PC "+str(current))

    #Set the voltage or current based on the device resistance
    def set_vc(self, current = None, voltage = None):

        if(current != None):
            if(voltage != None):
                self.set_output_curr(current)
                self.set_output_volt(voltage)
            else:
                self.set_output_curr(current)
                self.set_output_volt(current*self.status['Resistance'])
        else:
            self.set_output_volt(voltage)
            self.set_output_curr(voltage/self.status['Resistance'])
            
    # turn the output on or off
    def set_on(self, on):
        self.instrument.write('OUT '+str(on))

    def set_ovp(self, ovp):
        self.instrument.write("OVP "+str(ovp))

    ## Getters
    def query_output_voltage(self):
        self.status['Output_volt'] = float(self.instrument.query("PV?"))
        return self.status['Output_volt']

    # Get the set output current
    def query_output_current(self):
        self.status['Output_curr'] = float(self.instrument.query("PC?"))
        return self.status['Output_curr']

    # Get the true output current
    def query_meas_output_current(self):
        self.status['Meas_curr'] = float(self.instrument.query('MC?'))
        return self.status['Meas_curr']

    def query_meas_output_voltage(self):
        self.status['Meas_volt'] = float(self.instrument.query('MV?'))
        return self.status['Meas_volt']

    # Is the output turned on
    def query_output(self):
        self.status['Output'] = self.instrument.query('OUT?')
        return self.status['Output']

    # Find the devices resistance
    def query_resistance(self):
        # Find the outputed voltage and current
        self.get_meas_output_current()
        self.get_meas_output_voltage()
        self.status['Resistance'] = self.status['Meas_volt']/self.status['Meas_curr']
        
        return self.status['Resistance']

    def query_id(self):
        return self.instrument.query("IDN?")

    def query_ovp(self):
        self.status['OVP'] = float(self.instrument.query('OVP?'))
        return self.status['OVP']