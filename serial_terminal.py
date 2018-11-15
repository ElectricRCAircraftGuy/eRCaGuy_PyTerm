"""
serial_terminal.py

Gabriel Staples
14 Nov. 2018

References:
- https://pyserial.readthedocs.io/en/latest/pyserial_api.html

To install PySerial: `sudo python3 -m pip install pyserial`

To run this program: `python3 serial_terminal.py`

"""

import serial

def main():

    port = '/dev/ttyUSB1'
    baudrate = 115200

    ser = serial.Serial(
        port = port, 
        baudrate = baudrate,
        parity = serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        )

    print("Opening serial port using PySerial. serial.Version = {}".format(serial.VERSION))

    # Attempt twice
    for i in range(2):
        if (ser.isOpen() == True):
            print("Warning: serial port already open. Closing it now.")
            ser.close()

    if (ser.isOpen() == True):
        print("Warning: serial port already open. Closing it now.")
        ser.close()

    # print('Opening serial port "{}" at baudrate = {}.'.format(port, baudrate)
    # # ser.open()

    # keep_going = True
    # while(keep_going):
        # if (ser.in)



    # ser.close()

if (__name__ == '__main__'):
    main()