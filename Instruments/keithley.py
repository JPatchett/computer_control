import visa
import Instruments.instrument as inst

class keithley(inst.instrument):

    def __init__(self, address, rm, ide):

        super().__init__(address, rm, ide)


    

    ## Setters

    #reset
    def reset(self):
        self.instrument.write("*RST")

    # Set the output on
    def set_on(self, output):
        self.instrument.write(":OUTP:STAT "+str(output))

    # Set the source amplitude
    def set_source_ampl(self, channel, output):
        self.instrument.write(":SOUR:"+channel+":IMM:AMPL "+str(output))

    # Set the source range
    def set_source_range(self, channel, range):
        self.instrument.write(":SOUR:"+channel+":RANG "+str(range))

    # Set the source range to auto
    def set_source_range_auto(self, channel, auto):
        self.instrument.write(":SOUR:"+channel+":RANG:AUTO "+str(auto))

    #Set auto range for the current/voltage sensing on or off
    def set_auto(self, channel, auto):
        self.instrument.write(":SENS:"+str(channel)+":AUTO "+str(auto))
        self.status['Auto'] = auto

    #Set either current or voltage mode
    #CURR or VOLT
    def set_source_mode(self, mode):
        self.instrument.write("SOUR:FUNC:MODE "+str(mode)) 

    #Set the sense mode
    #N.b. this turns on this sense function, but does not turn off all the others
    def set_sense_mode(self, mode):
        self.instrument.write(":FUNC \""+str(mode)+"\"")

    #Set the delay
    def set_delay(self, delay):
        self.instrument.write(":DEL "-str(delay))

    #Set all the sense functions on (CURR:DC, VOLT:DC, RES)
    def sense_set_all(self):
        self.instrument.write(":SENS:FUNC:ON:ALL")

    ## Getters
    def query_sense_on(self):
        self.status['Sense_on'] = self.instrument.query(':SENS:FUNC:ON?')

    def read(self):
        self.status['Output'] = self.instrument.query(":OUTP?")
        return self.status['Output']