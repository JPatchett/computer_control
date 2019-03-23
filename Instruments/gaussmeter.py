import visa
import Instruments.instrument as inst

class gaussmeter_455(inst.instrument):

    def __init__(self, address, rm, ide):

        super().__init__(address, rm, ide)

        #Add the extra variables into the status dictonary
        self.status['Range'] = 0 #Range of the output
        self.status['Auto'] = 0 #Where the output range is automatically adjusted (recommended)
        self.status['Units'] = 0 #Units used in the output

        #Properly intialise all of the variables
        self.read() 
        self.query_range()
        self.query_auto()
        self.query_units()

    #Read and return the output
    def read(self):
        
        q_output = float(self.instrument.query('RDGFIELD?').rstrip('\r\n'))

        self.status['Output'] = q_output
        return q_output

    ##Setters
    ############################
    ## Takes either 1 (True) or 0 (False)
    def set_auto(self, auto):
        try:
            self.instrument.write("AUTO ",str(auto))
            self.query_auto()
        except(TypeError):
           print("Failed to change the auto-value to ",auto)

    #Set the range of the gaussmeter
    def set_range(self, ran):
        try:
            self.instrument.write("RANGE ",str(ran))
            self.query_range()
        except:
            print("Failed to change the range to ",ran)

    #1 GAUSS
    #2 TESLA
    #3 ORESTED
    #4 AMP/METRE
    def set_units(self, units):
        try:
            self.instrument.write("UNIT ",str(units))
            self.query_units()
        except:
            print("Failed to change the units to ",units)

    ##Query
    ############################
    def query_range(self):

        q_range = int(self.instrument.query('RANGE?').rstrip('\r\n'))
        self.status['Range'] = q_range
        return q_range

    def query_auto(self):

        q_auto = int(self.instrument.query('AUTO?').rstrip('\r\n'))
        self.status['Auto'] = q_auto
        return q_auto

    def query_units(self):
        
        q_units = int(self.instrument.query('UNIT?').rstrip('\r\n'))
        self.status['Units'] = q_units
        return q_units