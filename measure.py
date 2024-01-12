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
XMAX = 6e3  # in um
YMAX = 5e3  # in um
RES = 0.2e3  # spatial resolution in um
POSITIONS = [(x, y, 0) for x in np.arange(0, 2*XMAX+RES, RES) for y in np.arange(0, YMAX+RES, RES)]

# Device configs --
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

    # Measurement
    try:
        # Open the serial connection to the Virtual Com Port (VCP)
        ser = component.manipulator.Serial(**SERIAL_SETTINGS)

        # Configure
        print("Configure...")
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
        
        # goto((0, 0, 10000))
        
        for pos in POSITIONS:
            goto(pos)
            # for volt in VOLTAGES:
            #     mean, all_raw = record(volt, sleep_time=SLEEP_TIME)
            #     key = get_datakey(pos, volt)
            #     mean_data[key] = mean
            #     for i_raw, raw in enumerate(all_raw):
            #         all_data[key + f"_#{i_raw}"] = raw

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

if __name__ == "__main__":
    main()