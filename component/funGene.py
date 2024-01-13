import pyvisa
import sys

# Connection to the multifunction generator
try:
    print('test')
    rm = pyvisa.ResourceManager()
    func = rm.open_resource('USB0::0x0D4A::0x000D::9201982::INSTR')
    print('Connected to the multifunction generator')
    # func = rm.open_resource('USB0::0x0D4A::0x000D::9338635::INSTR')
except:
    print('Error: No connection to the multifunction generator')
    sys.exit(0)

def setFreq(freq):
    """
    Set the frequency of the multifunction generator.
    """
    print(f"Set frequency to {freq}kHz")
    func.write(f":SOURce1:FREQuency:FIXed {freq}k")

def setVolt(volt):
    """
    Set the voltage of the multifunction generator.
    """
    print(f"Set voltage to {volt} VPP")
    func.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {volt} VPP")

def setWaveform():
    """
    Set the waveform of the multifunction generator as continuous sinusoid wave.
    """
    print("Set waveform to continuous sinusoid wave")
    func.write(':SOURce1:CONTinuous:IMMediate')
    func.write(":SOURce1:FUNCtion:SHAPe SINusoid")

def setOutputOn():
    """
    Set the output state as ON.
    """
    func.write(':OUTPut1:STATe ON')
    func.write('*TRG')

def setOutputOff():
    """
    Set the output state as OFF.
    """
    func.write(":OUTPut1:STATe OFF")