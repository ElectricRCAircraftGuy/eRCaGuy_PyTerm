
import serial

# User Configuration Global "Constants":

# For testing purposes, where no real serial device is plugged in, set SIMULATE_SERIAL to True; set to False
# to actually communicate over a real, plugged-in serial device.
# SIMULATE_SERIAL = True
SIMULATE_SERIAL = False
LOG_FOLDER = './logs/' # log folder path relative to the main script
EXIT_COMMAND = "exit" # typed keyboard command from user to exit this program#####

# User Configuration Global Variables:

logger_is_on = True # for logging data to a file
line_ending = '\r' # Characters to append to all outgoing messages over serial

# Default serial settings used when not specified at the command line.
# See PySerial (Python serial library) documentation for options: 
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html
# - Note: the commonly-used "8N1" serial settings for devices means 8 data bits (bytesize), No parity bit, and 1 
#   stop bit. (See https://en.wikipedia.org/wiki/8-N-1).
serial_config = {
    'port': '/dev/ttyUSB1',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS, # 8
    'parity': serial.PARITY_NONE, # N
    'stopbits': serial.STOPBITS_ONE, # 1
    'timeout': None,
    'write_timeout': None,
}


