import component
import numpy as np
import time
import matplotlib.pyplot as plt
import os

# Plot settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = '14'
plt.rcParams['figure.subplot.bottom'] = '0.15'
plt.rcParams['figure.subplot.left'] = '0.2'

# Make a folder
if not os.path.exists(f'data/Figure'):
    os.makedirs(f'data/Figure')
if not os.path.exists(f'data/csv'):
    os.makedirs(f'data/csv')

# Parameters
FREQ = 500  # in kHz
VPP = 2  # in V
CH = 2  # channel
TRIALS = 3
XMAX = 6e3  # in um
YMAX = 5e3  # in um
RES = 1e3  # spatial resolution in um
POSITIONS = [(x, y, 0) for x in np.arange(0, 2*XMAX+RES, RES) for y in np.arange(0, YMAX+RES, RES)]
NAME = [f'{x*1e-3:.1f}_{y*1e-3:.1f}' for x in np.arange(0, 2*XMAX+RES, RES) for y in np.arange(0, YMAX+RES, RES)]

# Manipulator configs
SERIAL_SETTINGS = {
    "port": "COM7",
    "baudrate": 128000, # Data rate [bits/sec]
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
    "timeout": 10
}

Position = tuple[float, float, float]

def main():
    # Prepare data array
    # data = np.zeros((TRIALS, int((XMAX/RES)*2), int(YMAX/RES)))
    p_all = [[0] for k in range(TRIALS)]

    # Measurement
    try:
        # Open the serial connection to the Virtual Com Port (VCP)
        ser = component.manipulator.Serial(**SERIAL_SETTINGS)

        # Configure
        print("---Input settings---")
        component.funGene.setFreq(FREQ)
        component.funGene.setVolt(VPP)
        component.funGene.setWaveform()


        def goto(pos: Position, sleep_time: float = 0):
            """
            Move the manipulator to the specified position. Positions should be specified in micro-meters.
            """
            component.manipulator.set_position(ser, pos)
            print(f"Position set to {pos}.")
            time.sleep(sleep_time)
        
        n = 0
        for pos in POSITIONS:
            goto(pos)
            time.sleep(1)
            for k in range(TRIALS):
                # Record
                print(f"Recording trial {k+1}/{TRIALS}...")
                component.funGene.setOutputOn()
                time.sleep(0.5)
                component.oscilloscope.timeout = None  # Set timeout to infinite
                data = component.oscilloscope.record(ch=2)
                component.funGene.setOutputOff()

                time.sleep(1)
                p_all[k] = data[:, 1]

            p_all = np.array(p_all)
            p_mean = np.mean(p_all, axis=0)

            t = data[:, 0]
            t = np.array(t)
            p_arr = np.array(p_all[0])
            t_arr = t
            for k in range(TRIALS-1):
                p_arr = np.append(p_arr, p_all[k+1, :])
                t_arr = np.append(t_arr, t)
            
            # Figure
            plt.subplot(211)
            plt.title('Signal')
            plt.ylabel('Voltage (mV)')
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.tick_params(labelbottom=False, labelleft=True, labelright=False, labeltop=False)
            for k in range(TRIALS):
                plt.plot(t*1e6, p_all[k, :]*1e3, color='black', alpha=0.25)

            plt.subplot(212)
            plt.plot(t*1e6, p_mean*1e3, color='black')
            plt.title('Mean signal')
            plt.ylabel('Voltage (mV)')
            plt.xlabel('Time (\u03bcs)')
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)

            plt.subplots_adjust(hspace=0.4)
            plt.savefig(f'data/Figure/{NAME[n]}.png')
            plt.close()

            #csv
            save_csv = np.c_[t_arr, p_arr]
            np.savetxt(f'data/csv/{NAME[n]}.csv', save_csv, delimiter=',')
            n += 1

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    
    # Shut down serial connection
    finally:
        # Check if the Serial is instanciated
        if not isinstance(ser, component.manipulator.Serial):
            print("No serial connection.")
            return

        # Go to home positiong
        component.manipulator.set_position_to_home(ser)

        # Close the connection
        ser.close()

        # Turn off the function generator
        component.funGene.setOutputOff()

if __name__ == "__main__":
    main()