import pyvisa
import sys

# Connection to the multifunction generator
try:
    rm = pyvisa.ResourceManager()
    func = rm.open_resource('USB0::0x0D4A::0x000D::9201982::INSTR')
    # func = rm.open_resource('USB0::0x0D4A::0x000D::9338635::INSTR')
except:
    print('Error: No connection to the multifunction generator')
    sys.exit(0)

def setFreq(freq):
    print(f"Set frequency to {freq}kHz")
    func.write(f":SOURce1:FREQuency:FIXed {freq}k")

def setVolt(volt):
    print(f"Set voltage to {volt} VPP")
    func.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {volt} VPP")

def setWaveform():
    print("Set waveform to continuous sinusoid wave")
    func.write(':SOURce1:CONTinuous:IMMediate')
    func.write(":SOURce1:FUNCtion:SHAPe SINusoid")