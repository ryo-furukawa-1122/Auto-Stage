import numpy as _np
import struct as _struct
import serial as _serial

from numpy.typing import ArrayLike as _ArrayLike
from typing import Literal as _Literal

CONV_FACT = 0.0625 # 1 microstep = 0.0625 micrometers
ENDBYTE = b"\r"

# Classes -----
Serial  = _serial.Serial

# Data conversion -----

def _usteps2um(usteps: int):
    """
    Convert microsteps (usteps) to micro-meters (um) 
    """
    return round(usteps * CONV_FACT)

def _um2usteps(um: float):
    """
    Convert micro-meters (um) to microsteps (usteps)
    """
    return round(um / CONV_FACT)

def _val2bytes(val):
    """
    Pack value to bytes
    """
    return _struct.pack("<l", val)

def _bytes2val(b: bytes):
    """
    Unpack byte values
    """
    return _struct.unpack("<l", b)

def _bytes2um(b: bytes):
    """
    Unpack bytes and convert to micro-meters
    """
    return _usteps2um(_bytes2val(b)[0])

def _um2bytes(um: float):
    """
    Pack micro-meter values to bytes
    """
    return _val2bytes(_um2usteps(um))


# Commands -----

def send_command(ser: Serial, command: bytes):
    """
    Send command to the connected serial port
    """
    ser.write(command)
    res = ser.read_until(ENDBYTE)
    return res

def change_drive(ser: Serial, drive_num: _Literal[1, 2, 3, 4]):
    """
    Change the drive (manipulator)
    """
    if drive_num not in [1, 2, 3, 4]:
        raise ValueError(f"Drive number should be either 1, 2, 3 or 4, got {drive_num}.")

    command = bytes(f"I{drive_num:02X}", "utf-8")
    send_command(ser, command) 

def get_position(ser: Serial, print_info: bool = False):
    """
    Read the current position of the manipulator
    """
    res = send_command(ser, b"C")
    res = res[1:]

    # Get data for each coordinate
    pos_data = [ res[:4], res[4: 8], res[8:12] ]

    # Convert bytes to position
    position = _np.array([
        _bytes2um(data)
        for data in pos_data
    ])

    if print_info:
        pos_keys = ["x", "y", "z"]

        # Print bytes
        print("Recieved bytes (little endian)")
        for key, data in zip(pos_keys, pos_data):
            hex = data.hex()
            hex_str = "0x" + ", 0x".join([hex[i:i+2] for i in range(0, len(hex), 2)])
            print(f"{key}:", hex_str)
        print()
    
        # Print position
        print("Current position")
        for k, v in zip(pos_keys, position):
            print(f"{k}:", v, end="  ")
        print(end="\n\n")

    return position

def set_position(ser: Serial, position: _ArrayLike):
    """
    Set the position of the manipulator
    """
    position = _np.array(position)
    if position.shape != (3,):
        raise ValueError("The position should be a np array with shape (3,).")
    
    # Convert micro-meter values to bytes for each coordinate
    position_bytes = [_um2bytes(p) for p in position]

    # Create the command
    command = b"M" + b"".join(position_bytes) + b"\x0d"

    # Send the command
    send_command(ser, command)

def set_position_to_home(ser):
    """
    Set current position to home (0, 0, 0)
    """
    send_command(ser, b"H")

def set_work_position(ser):
    """
    Set current position as work position
    """
    send_command(ser, b"Y")

def center_drive(ser: Serial):
    """
    Reset (center) the drive position
    """
    send_command(ser, b"N")

def interrupt_drive(ser: Serial):
    """
    Interrupt drive movement
    """
    send_command(ser, b"\x03") # Control-C in bytes