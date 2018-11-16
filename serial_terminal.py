"""
serial_terminal.py

Gabriel Staples
14 Nov. 2018

References:
- https://pyserial.readthedocs.io/en/latest/pyserial_api.html

To install PySerial: `sudo python3 -m pip install pyserial`

To run this program: `python3 serial_terminal.py`

"""

import time
import serial

def main():

    # Open serial port
    # Note: The port is immediately opened on object creation when a port is given. See:
    # https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
    port = '/dev/ttyUSB1'
    baudrate = 115200

    print('Opening serial port using PySerial. serial.Version = {}\n'
          '  port = "{}", baudrate = {}'.format(serial.VERSION, port, baudrate))

    ser = serial.Serial(
        port = port, 
        baudrate = baudrate,
        parity = serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        )

    while (True):
        if (ser.inWaiting() > 0):
            data_str = ser.read(ser.inWaiting()).decode('ascii')
            print(data_str, end='') 
        

        # Sleep for a short time to prevent this thread from sucking up all of your CPU resources on your PC.
        time.sleep(0.01) 




    ser.close()

if (__name__ == '__main__'):
    main()