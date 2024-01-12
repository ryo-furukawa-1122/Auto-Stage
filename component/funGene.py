import pyvisa
import sys

# Connection to the multifunction generator
try:
    rm = pyvisa.ResourceManager()
    func = rm.open_resource('USB0::0x0D4A::0x000D::9201982::INSTR')
    func = rm.open_resource('USB0::0x0D4A::0x000D::9338635::INSTR')
except:
    print('Error: No connection to the multifunction generator')
    sys.exit(0)
