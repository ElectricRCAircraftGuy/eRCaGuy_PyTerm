
# Internal Modules
import user_config

# External Modules
import datetime # to create log file name based on current date and time
import os # to get absolute paths

class Logger:
    "Class for logging to a file"
    
    def __init__(self, print_func=None, spaces=None):
        "Logger constructor"
        self.logging_on = user_config.LOGGING_ON
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
            
        if (self.logging_on):
            self.open()
    
    def open(self):
        "Open file for logging"
        
        # Only open a file for logging if one isn't already open
        if (self.log_file):
            return

        # Get a filename, in desired format. 
        # See: https://stackoverflow.com/a/32490661/4561887 and http://strftime.org/
        filename = datetime.datetime.today().strftime('%Y%m%d-%H%Mhrs%Ssec_serialdata.txt')
        self.log_file_path = user_config.LOG_FOLDER + filename
        #Absolute path; see: https://stackoverflow.com/a/51523/4561887
        self.log_file_path_abs = os.path.abspath(self.log_file_path)
        
        if (self.print_func):
            self.print_func(('Opening log file: logging all messages to\n' + 
                             self.spaces + '"{}".').format(self.log_file_path))

        self.log_file = open(self.log_file_path, "w")
    
    def close(self):
        "Close log file"
        
        if (self.log_file):
            if (self.print_func):
                self.print_func(('Opening log file: logging all messages to\n' + 
                             self.spaces + '"{}".').format(self.log_file_path))
            self.log_file.close()
            self.log_file = None
    
    def write(self, string):
        "Write to the log file"
        
        if (self.log_file):
            self.log_file.write(string)
            
    def printAndWrite(selfs, string):
        "Print to stdout *and* write to the log file"
        pass
    
    def setLogging(self, logging_on):
        "Turn logger on or off"
        self.logging_on = logging_on
        
if (__name__ == '__main__'):
    logger = Logger()
    logger.open()
    logger.write("test write\n")
    logger.printAndWrite("test print and write\n")


