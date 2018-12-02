
import serial

# User Configuration Global variables:

# For testing purposes, where no real serial device is plugged in, set to False; set to True to actually communicate
# over a plugged-in serial device.
REAL_SERIAL = False
LOGGING_ON = True # for logging data to a file
LOG_FOLDER = './logs/'
EXIT_COMMAND = "exit" # Command to exit this program

# Default serial settings used when not specified at the command line.
# See PySerial (Python serial library) documentation for options: 
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html
# Note: 8N1 (https://en.wikipedia.org/wiki/8-N-1) means 8 data bits (bytesize), No parity bit, and 1 stop bit.
serial_config = {
    'port': '/dev/ttyUSB1',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
}


