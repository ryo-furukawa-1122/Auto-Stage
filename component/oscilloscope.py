import pyvisa
import sys

# Connection to the oscilloscope
try:
    rm = pyvisa.ResourceManager()
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
except:
    print('Error: No connection to the osci')
    sys.exit(0)

def record(ch):
    fs = osci.query('SARA?')
    fs = fs[len('SARA '):-5]
    fs = float(fs)

    vd = osci.query(f'C{ch}:VDIV?')
    vd = vd[len(f'C{ch}:VDIV '):-2]
    vd = float(vd)

    voff = osci.query(f'C{ch}:OFST?')
    voff = voff[len(f'C{ch}:OFST '):-2]
    voff = float(voff)