import visa
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.anritsu import AnritsuMG3692C
from time import sleep
import keithly2000 as k2

#Find all the GPIB connected devices
rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
print(rm.list_resources())

volt_range = 200e-3



keith = k2.keithly("GPIB0::28::INSTR", rm)

keith.source("volt")
keith.src_range(k2.SRC_V_RAN.mV200)
keith.src_level(8e-3)

keith.measure("curr")
keith.measure_range(k2.MEAS_I_RAN_CP.mA100)
keith.write(":TRIG:COUN 1")
keith.write(":FORM:ELEM CURR")
keith.set_output(True)
print(keith.read())

