import Instruments.instrument as inst
import visa 
import numpy as np
import re
import time

class lockIn(inst.instrument):

    def __init__(self, address, rm, id, reset = True):

        super().__init__(address, rm, id)

        self.reset(reset)

    ##AQUIRE DATA
    #Read the X/Y/R/theta data
    def read(self, component):
        return self.instrument.query('OUTP?'+str(component))

    #Read from channel 1 or 2
    def read_ch(self, channel):
        return self.instrument.query('OUTR?'+str(channel))
    

    def reset(self, reset):
        if(reset):
            self.instrument.write('*RST')
            
        time.sleep(0.2)
        self.query_phase() #Phase shift of the lock-in
        time.sleep(0.2)
        self.query_ref_src() #0 for internal, 1 for external
        time.sleep(0.2)
        self.query_ref_freq() #Frequency of the internal reference source
        time.sleep(0.2)
        self.query_harmonics() #The harmonics the lock in will detect
        time.sleep(0.2)
        self.query_time_const() #Set the time constant for integratio from 0-19, takes aronud 5 time constants to settle
        time.sleep(0.2)
        self.query_filter_slope() #Set the low pass filter slope to 6,12,18 or 24 dB/Oct (0-3)
        time.sleep(0.2)
        self.query_sync() #Set the synchronous filter to off or on below 200Hz
        time.sleep(0.2)
        self.query_I_src() #Set the source to A,A-B , I, I high impedance (0-3)
        time.sleep(0.2)
        self.query_ground() #Set the grounding to float to or ground
        time.sleep(0.2)
        self.query_ch_1() #Set the display to X, Y, R, theta, noise etc.
        time.sleep(0.2)
        self.query_ch_2() #Same for channel two
        time.sleep(0.2)
        self.query_dyn_res() #Dynamic reserve either hugh, normal, or low noise (0-2)
        time.sleep(0.2)
        self.query_sens()  #Set the senstivity
        time.sleep(0.2)
        self.query_offset() #Set the offset
        time.sleep(0.2)
        self.query_expand() #Set the expand

    ##SETTERS
    ##AUTO
    #Let the lock in automatically set various settings
    #Offset
    def auto_off(self, channel):
        self.instrument.write('AOFF'+str(channel))
        self.query_offset()

    #Gain
    def auto_gain(self):
        self.instrument.write('AGAN')

    #Dynamic reserve
    def auto_reserve(self):
        self.instrument.write('ARSV')
        self.query_phase()

    #Phase
    def auto_phase(self):
        self.instrument.write('APHS')
        self.query_phase()

    ##MANUAL
    def set_phase(self, phase):
        self.instrument.write('PHAS{'+str(phase)+'}')
        self.query_phase()

    #Set the expand parameter for the X/Y/R channel
    def set_expand(self, expand, channel):
        self.instrument.write('OEXP'+str(channel)+'{,'+str(self.status['Offset'][channel-1])+','+str(expand)+'}')
        self.query_expand() #update our status dictonary

    #Same for offset
    def set_offset(self, offset, channel):
        self.instrument.write('OEXP'+str(channel)+'{,'+str(offset)+','+str(self.status['Expand'][channel])+'}')
        self.query_offset()
    
    def set_rf_src(self, src):
        self.instrument.write('FMOD '+str(src))
        self.query_ref_src()
    
    def set_rf_freq(self, freq):
        self.instrument.write('FREQ '+str(freq))
        self.query_ref_freq()

    def set_harmonic(self, harmonic):
        self.instrument.write('HARM{'+str(harmonic)+'}')
        self.query_harmonics()
    
    def set_I_scr(self, I_scr):
        self.instrument.write('ISRC{'+str(I_scr)+'}')
        self.query_I_src()

    def set_ground(self, ground):
        self.instrument.write('IGND '+str(ground))
        self.query_ground()

    def set_sens(self, sens):
        self.instrument.write('SENS '+str(sens))
        self.query_sens()
    
    def set_dyn_res(self, dyn_res):
        self.instrument.write('RMOD{'+str(dyn_res)+'}')
        self.query_dyn_res()

    def set_time_const(self, time_const):
        self.instrument.write('OFLT '+str(time_const))
        self.query_time_const()
    
    def set_filter_slope(self, filt):
        self.instrument.write('OFSL '+str(filt))
        self.query_filter_slope()
    
    def set_sync(self, sync):
        self.instrument.write('SYNC '+str(sync))
        self.query_sync()
    
    def set_ch_1(self, ch_1):
        self.instrument.write('DDEF1{,'+str(ch_1)+',0}')
        self.query_ch_1()

    def set_ch_2(self, ch_2):
        self.instrument.write('DDEF2{,'+str(ch_2)+',0}')
        self.query_ch_2()


    ##GETTERS
    def query_phase(self):
        self.status['Phase'] = float(self.instrument.query('PHAS?'))
        return self.status['Phase']

    def query_ref_src(self):
        self.status['Ref_source'] = int(self.instrument.query('FMOD?'))
        return self.status['Ref_source']

    def query_ref_freq(self):
        self.status['Ref_freq'] = float(self.instrument.query('FREQ?'))
        return self.status['Ref_freq']

    def query_harmonics(self):
        self.status['Harmonics'] = int(self.instrument.query('HARM?'))
        return self.status['Harmonics']

    def query_time_const(self):
        self.status['Time_const'] = int(self.instrument.query('OFLT?'))
        return self.status['Time_const']

    def query_filter_slope(self):
        self.status['Filter_slope'] = int(self.instrument.query('OFSL?'))
        return self.status['Filter_slope']
    
    def query_sync(self):
        self.status['Sync'] = int(self.instrument.query('SYNC?'))
        return self.status['Sync']

    def query_I_src(self):
        self.status['I_src'] = int(self.instrument.query('ISRC?'))
        return self.status['I_src']

    def query_ground(self):
        self.status['Ground'] = int(self.instrument.query('IGND?'))
        return self.status['Ground']

    def query_ch_1(self):
        self.status['Ch_1'] = int(self.instrument.query('DDEF?1')[0])
        return self.status['Ch_1']
    
    def query_ch_2(self):
        self.status['Ch_2'] = int(self.instrument.query('DDEF?2')[0])
        return self.status['Ch_2']

    def query_sens(self):
        self.status['Sens'] = int(self.instrument.query('SENS?'))
        return self.status['Sens']

    def query_dyn_res(self):
        self.status['Dyn_res'] = int(self.instrument.query('RMOD?'))
        return self.status['Dyn_res']

    def query_offset(self):
        x_ch = self.instrument.query('OEXP?1')
        y_ch = self.instrument.query('OEXP?2')
        r_ch = self.instrument.query('OEXP?3')

        x_ch = re.search(r'[-]?[\d.]*', x_ch).group(0)
        y_ch = re.search(r'[-]?[\d.]*', y_ch).group(0)
        r_ch = re.search(r'[-]?[\d.]*', r_ch).group(0)


        self.status['Offset'] = np.array([float(x_ch), float(y_ch), float(r_ch)])

        return self.status['Offset']

    def query_expand(self):
        x_ch = self.instrument.query('OEXP?1')
        y_ch = self.instrument.query('OEXP?2')
        r_ch = self.instrument.query('OEXP?3')

        self.status['Expand'] = np.array([int(x_ch[-2]), int(y_ch[-2]), int(r_ch[-2])])

        return self.status['Expand']

    #Query the control bits
    #gets the 1st bit of the serial poll status bit that indicates if a comman is being executed
    def busy(self):
        SPSB = int(self.instrument.query('*SRE? 1'))
        return SPSB
        

        