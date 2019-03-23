##Superclass for GPIB connected instruments
##Created by James Patchett
##01/03/19

class instrument:

    ##Constructor
    #############################
    def __init__(self, address, rm, ide, rm_args = None):
        
        #Open the instrument
        try:
            self.__id = ide #ID of the instrument
            self.__address = address #GPIB address

            if(rm != None):
                self.__rm = rm #The Visa resource manager

                if(rm_args == None):
                    self.instrument = self.__rm.open_resource(self.__address) #Open comms to the instrument
                else:
                    self.instrument = self.__rm.open_resource(self.__address, **rm_args) #Open the instrument with optional arguments
        except: 
            print("Instrument ", ide, " could not be opened")
            self.address = None
            self.rm = None

        #Intialise other variables
        self.status = {"Address":self.__address, "Identity":self.__id, "Output":0} #Contains all the relevant info about the instrument

    ##Querys
    ############################
    def query_id(self):
        return self.instrument.query('*IDN?')

    def read(self): #:OVERWRITE: Read data from the device 
        pass