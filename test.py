import visa
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.anritsu import AnritsuMG3692C
from time import sleep
import keithly2000 as k2

#Find all the GPIB connected devices
rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
print(rm.list_resources())

volt_range = 200e-3

#keith = rm.open_resource("GPIB0::28::INSTR")
#keith.write("*RST")
#keith.write(":SENS:FUNC:CONC OFF")
#keith.write(":SOUR:FUNC CURR")
#keith.write(":SENSE:FUNC \"VOLT\"")
#keith.write(":SOUR:CURR:START 1E-6")
#keith.write(":SOUR:CURR:STOP 10E-6")
#keith.write(":SOUR:CURR:STEP 1E-6")
#keith.write(":SOUR:CURR:MODE SWE")
#keith.write(":SOUR:SWE:RANG AUTO")
#keith.write(":SOUR:SWE:SPAC LIN")
#keith.write(":TRIG:COUN 10")
#keith.write(":SOUR:DEL 0.1")
#keith.write(":OUTP ON")
#print(keith.query(":READ?"))


#keith.write(":SOUR:FUNC VOLT")
#keith.write(":SOUR:VOLT 1e-3")
#keith.write(":SENS:FUNC \"CURR\"")
#keith.write(":SENS:CURR:RANG 10E-3")
#keith.write(":DISP:DIG 5")
#keith.write(":OUTP ON")
#print(keith.query(":READ?"))
#keith.write(":OUTP OFF")

keith = k2.keithly("GPIB0::28::INSTR", rm)

keith.source("curr")
keith.measure("volt")
x = keith.linear_sweep(1e-6, 10e-6, 1e-6, delay = 100)
print(x)
#keith.src_range(k2.SRC_V_RAN.mV200)

#keith.measure("curr")
#keith.measure_range(k2.MEAS_I_RAN_CP.A1)

#print(keith.linear_sweep(0, 8e-3, 9, delay = 100))
#keith.set_output(False)
