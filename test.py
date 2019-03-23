import visa
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.anritsu import AnritsuMG3692C
from time import sleep

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
print(rm.list_resources())


inst = rm.open_resource("GPIB0::28::INSTR")
print(inst.query("*IDN?"))

inst.write(":SOUR:FUNC CURR")