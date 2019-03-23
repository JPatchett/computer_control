import visa
import Instruments.instrument as inst

class anritsu(inst.instrument):

    def __init__(self, address, rm, ide, reset = True):

        super().__init__(address, rm, ide)
        
        print("Intailising "+ide+ " status variables")
        #Reset the source and intialise all variables
        if(reset):
            self.reset()
        else:
            #Intialise all variables
            self.query_output_on() #Whether or not the instrument is outputnig power
            self.query_output_prot() #Turn the output off whilst changnig frequency
            self.query_freq() #Frequency of the outputted signal (GHZ)
            self.query_freq_mode() #Sets which frequency mode the instrument is on (fixed, sweep etc.)
            self.query_sweep_start() #Starting and ending frequencies for the frequency sweep
            self.query_sweep_stop()
            self.query_sweep_step() #Frequency incriments for the sweep
            self.query_power() #Output power of the machine
            self.query_pulse_on() #Pulse modulation on or off
            self.query_pulse_sour() #Sets the sourec of the pulse modulation

        #Set the protection on
        #Do not disable without good reason
        self.set_output_prot(1)

    def reset(self):
        self.instrument.write('*RST')

        #Reset all the status commands
        self.query_output_on() #Whether or not the instrument is outputnig power
        self.query_output_prot() #Turn the output off whilst changnig frequency
        self.query_freq() #Frequency of the outputted signal (GHZ)
        self.query_freq_mode() #Sets which frequency mode the instrument is on (fixed, sweep etc.)
        self.query_sweep_start() #Starting and ending frequencies for the frequency sweep
        self.query_sweep_stop()
        self.query_sweep_step() #Frequency incriments for the sweep
        self.query_power() #Output power of the machine
        self.query_pulse_on() #Pulse modulation on or off
        self.query_pulse_sour() #Sets the sourec of the pulse modulation

    ##SETTERS
    #Turn the output on or off
    def set_output_on(self, on):
        self.status['On'] = on
        self.instrument.write(':OUTP:STAT '+str(on))

    #Whether or not the output should be switched off during frequency changes
    #Do not turn off without good reason
    def set_output_prot(self, prot):
        self.status['Output_prot'] = prot
        self.instrument.write(':OUTP:PROT '+str(prot))

    #Set the frequency (GHz)
    def set_freq(self, freq):
        self.status['Frequency'] = freq
        self.instrument.write(':FREQ '+str(freq)+' GHz')

    #E.g. FIX, SWE, LIST
    def set_freq_mode(self, freq_mode):
        self.status['Freq_mode'] = freq_mode
        self.instrument.write(':FREQ:MODE '+str(freq_mode))

    #Starting and ending frequencies for the frequency sweep mode (GHz)
    #####
    def set_sweep_start(self, freq):
        self.status['Sweep_start'] = freq
        self.instrument.write(':FREQ:STAR '+str(freq)+' GHz')

    def set_sweep_stop(self, freq):
        self.status['Sweep_stop'] = freq
        self.instrument.write(':FREQ:STOP '+str(freq)+' GHz')
    #####

    #Set the step of the sweep mode
    def set_sweep_step(self, freq):
        self.status['Sweep_step'] = freq
        self.instrument.write(':FREQ:STEP '+str(freq))

    #Set the power output in dBm
    def set_power(self, power):
        self.status['Power'] = power
        self.instrument.write(':POW:LEV:IMM:AMPL '+str(power)+' dBm')

    #Set pulse modulation on or off
    def set_pulse_on(self, on):
        self.status['Pulse_on'] = on
        self.instrument.write(':PULM:STAT '+str(on))
    
    #Set the source of the pulse modulation
    #INTernal1, INTernal2, EXTernal1, EXTernal2
    #EXTernal2 for the rear input
    def set_pulse_sour(self, source):
        self.status['Pulse_sour'] = source
        self.instrument.write(':PULM:SOUR '+str(source))

    ##QUERY
    def query_output_on(self):
        self.status['On'] = int(self.instrument.query(':OUTP:STAT?'))
        return self.status['On']

    def query_output_prot(self):
        self.status['Output_prot'] = int(self.instrument.query(':OUTP:PROT?'))
        return self.status['Output_prot']

    def query_freq(self):
        self.status['Frequency'] = float(self.instrument.query(':FREQ?'))
        return self.status['Frequency']

    def query_freq_mode(self):
        self.status['Freq_mode'] = self.instrument.query(':FREQ:MODE?')
        return self.status['Freq_mode']

    def query_sweep_start(self):
        self.status['Sweep_start'] = float(self.instrument.query(':FREQ:STAR?'))
        return self.status['Sweep_start']

    def query_sweep_stop(self):
        self.status['Sweep_stop'] = float(self.instrument.query(':FREQ:STOP?'))
        return self.status['Sweep_stop']

    def query_sweep_step(self):
        self.status['Sweep_step'] = float(self.instrument.query(':FREQ:STEP?'))
        return self.status['Sweep_step']

    def query_power(self):
        self.status['Power'] = float(self.instrument.query(':POW:LEV:IMM:AMPL?'))
        return self.status['Power']

    def query_pulse_on(self):
        self.status['Pulse_on'] = float(self.instrument.query(':PULM:STAT?'))
        return self.status['Pulse_on']

    def query_pulse_sour(self):
        self.status['Pulse_sour'] = self.instrument.query(':PULM:SOUR?')
        return self.status['Pulse_sour']