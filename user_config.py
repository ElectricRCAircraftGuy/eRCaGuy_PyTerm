
# User Configuration Global variables:

# -----------------------------------------------------------
# General settings
# -----------------------------------------------------------

# For testing purposes, where no real serial device is plugged in, set to False; set to True to
# actually communicate over a plugged-in serial device.
REAL_SERIAL = True
LOGGING_ON = True  # log all incoming serial data to a file
LOG_FOLDER = './logs/'
EXIT_COMMAND = "exit" # Command to exit this program

# Default serial settings used when not specified at the command line:
# port = '/dev/ttyUSB1'   # example on Linux
port = 'COM3'             # example on Windows
# common values are 9600, 115200, 230400, 250000, 500000, 1000000, etc.
baudrate = 230400 

# -----------------------------------------------------------
# Advanced settings
# -----------------------------------------------------------

# Choose how to print the data to your terminal and log it to the file. 
# Set to "ASCII" or "REPR".
# "ASCII" prints the text as normal ASCII characters. "\n", for instance, is a new-line. 
# "REPR" will call `repr()` on the data before printing it, meaning that a `\n` will print
# as a literal `\` char followed by an `n` char.
PRINT_FORMAT = "ASCII"  # default
# PRINT_FORMAT = "REPR" 

# Set to True to replace all instance of `\r\n` in the serial stream with just `\n`, and 
# set to False to leave the data alone as-is. This only has an effect if `PRINT_FORMAT`
# is set to "ASCII". 
REPLACE_BACKLASH_r_n = True
