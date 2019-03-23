import matlab.engine
import time
import Instruments.instrument as inst

##Class for the python control of the motor
##Requires MATLAB 2018 pr later to work, with matlab.engine installed
##On this machine

class motor(inst.instrument):

    def __init__(self, engine, ide):
        
        super().__init__(None, None, ide)

        #Set up the connection to MATLAB
        self.engine = engine


        #Intialise the connection with the motor
        self.engine.APTmotor(nargout = 0) #N.b if MATLAB can't find this file may need to use engine.addpath(path, nargout = 0)

        #Find the angle of the motor
        self.engine.getAngle() 

    ##SETTERS
    #Move the motor through the angle angle
    def move_Rel(self, angle):
        self.status['Angle']= self.engine.moveRel(angle)

    #Move the motor to the position defined by pos
    def move_abs(self, pos):
        self.status['Angle'] = self.engine.moveAbs(pos)

    ##GETTERS
    def getPos(self):
        self.status['Angle'] = self.engine.getAngle()
        return self.status['Angle']

    def getAngle(self):
        self.status['Angle'] = self.engine.getAngle() 
        return self.status['Angle']

    
