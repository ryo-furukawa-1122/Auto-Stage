import component
import numpy as np
import time
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = '14'

# Parameters
FREQ = 500  # in kHz
VPP = 2  # in V
CH = 2  # channel
TRIALS = 1
XMAX = 6  # in mm
YMAX = 5  # in mm
RES = 0.2  # spatial resolution in mm
POSITIONS = [[(x, y, 0) for x in range(-XMAX, XMAX+RES, RES) for y in range(0, YMAX+RES, RES)]]

def main():
    # Prepare data array
    data = np.zeros((TRIALS, RES*XMAX*2, RES*YMAX))

    # Measurement
    try:
        # Configure
        component.funGene.setFreq(FREQ)
        component.funGene.setVolt(VPP)
        component.funGene.setWaveform()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")