
# Internal Modules
import user_config

# External Modules
import datetime # to create log file name based on current date and time
import os # to get absolute paths

class Logger:
    "Class for logging to a file."
    
    def __init__(self, print_func=None, spaces=None):
        "Logger constructor"
        self.logger_is_on = user_config.logger_is_on
        self.log_file = None
        
        if (print_func):
            self.print_func = print_func
        else:
            # Default print function
            self.print_func = print
        
        if (spaces):
            self.spaces = spaces 
        else:
            # Default spaces string
            self.spaces = ' '*2
            
        if (self.logger_is_on):
            self.open()
    
    def open(self):
        "Open a log file (if one isn't already open)."
        
        # Only open a file for logging if one isn't already open
        if (self.log_file):
            self.print("ERROR: log file already opened.\n")
            return

        # Get a filename, in desired format. 
        # See: https://stackoverflow.com/a/32490661/4561887 and http://strftime.org/
        filename = datetime.datetime.today().strftime('%Y%m%d-%H%Mhrs%Ssec_serialdata.txt')
        self.log_file_path = user_config.LOG_FOLDER + filename
        #Absolute path; see: https://stackoverflow.com/a/51523/4561887
        self.log_file_path_abs = os.path.abspath(self.log_file_path)
        
        self.print(('Opening log file at\n' + 
                    self.spaces + '"{}".\n').format(self.log_file_path_abs))

        self.log_file = open(self.log_file_path, "w")
        
        self.printAndWrite(('Log file is open: logging all messages to\n' + 
                            self.spaces + '"{}".\n').format(self.log_file_path_abs))
    
    def close(self):
        "Close log file (if one is open)."
        
        if (not self.log_file):
            self.print("ERROR: no open log file to be closed.\n")
            return
        
        self.printAndWrite(('Closing log file: messages were logged to\n' + 
                            self.spaces + '"{}".\n').format(self.log_file_path_abs))
        self.log_file.close()
        self.log_file = None
    
    def print(self, string):
        "Print to print_func (stdout by default), with NO '\n' appended to the end."
        
        self.print_func(string, end='')
    
    def write(self, string):
        "Write to the log file."
        
        if (not self.log_file):
            self.print("ERROR: no open log file to write to.\n")
            return
        
        self.log_file.write(string)
        
    def writeIfOn(self, string):
        "Write to the log file, but ONLY IF the logger is on!"
        
        if (self.logger_is_on):
            self.write(string)
            
    def printAndWrite(self, string):
        "Print to print_func (stdout by default) *and* write to the log file."
        
        self.print(string)
        self.write(string)
        
    def printAndWriteIfOn(self, string):
        "Print no matter what, and write to the log file also, but ONLY IF the logger is on!"
        
        self.print(string)
        self.writeIfOn(string)
    
    def setLogging(self, logger_is_on):
        "Turn logger on or off. If turning it on, open a log file if one isn't already open."
        
        self.logger_is_on = logger_is_on
        
        # Create a new log file if one isn't open yet
        if (not self.log_file):
            self.open()
        
# Run the following test with `python3 logger.py` (Linux), or the equivalent command for your operating system.
if (__name__ == '__main__'):
    logger = Logger()
    logger.open() # Not necessary if user_config.LOGGING_ON == True
    logger.print("doing a test write\n")
    logger.write("test write\n")
    logger.print("test write done\n")
    logger.printAndWrite("test print and write\n")
    logger.printAndWriteIfOn("testing print and write if on\n")
    logger.close()


