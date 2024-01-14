import pyvisa
import sys
import numpy as np

# Connection to the oscilloscope
try:
    rm = pyvisa.ResourceManager()
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
    print('Connected to the oscilloscope')
except:
    print('Error: No connection to the oscilloscope')
    sys.exit(0)

def record(ch):
    osci.timeout = None

    # fs = osci.query('SARA?')
    # print(fs)
    # fs = fs[len('SARA '):-5]
    # fs = float(fs)
    fs = 500e6  # in Hz

    vd = osci.query(f'C{ch}:VDIV?')
    vd = vd[len(f'C{ch}:VDIV '):-2]
    vd = float(vd)

    voff = osci.query(f'C{ch}:OFST?')
    voff = voff[len(f'C{ch}:OFST '):-2]
    voff = float(voff)

    osci.write('TRMD NORM')
    osci.write('WFSU SP, 1, NP, 0, FP, 0')
    osci.write(f'C{ch}:WF? DAT2')
    osci.chunk_size = 1024**3

    wave = osci.query_binary_values(f'C{ch}:WF? DAT2', datatype='b', is_big_endian=True)

    wave = list(map(float, wave))
    wave = np.array(wave)
    v = wave * (vd / 25) - voff  # in V

    x = np.arange(0, len(wave), 1)
    t = x/fs  # in s

    return np.c_[t, v]