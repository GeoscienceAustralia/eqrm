
"""
Don't use this.
I realised I would have to pass instances of the class around.
And that is a pain.
Use log in ANUGA_utilities.
"""

import os
import sys
import logging

from eqrm_code.eqrm_filesystem import eqrm_path

DEFAULT_LOG_NAME = 'analysis'
DEFAULT_CONSOLE_LOG_LEVEL = logging.INFO
DEFAULT_FILE_LOG_LEVEL = logging.DEBUG
FMT = '%(asctime)s %(levelname)-8s |%(message)s'

 

class Log(object):
    logger_id = 0
    def __init__(self,
                 logger_id=None,
                 console_logging_level=DEFAULT_CONSOLE_LOG_LEVEL,
                 file_logging_level=DEFAULT_FILE_LOG_LEVEL,
                 default_to_console=True,
                 log_file_path=None):
        if logger_id is None:
            self.logger_id = str(self.__class__.logger_id)
            self.__class__.logger_id += 1
        else:
            self.logger_id = logger_id
        self.console_logging_level = console_logging_level
        self.file_logging_level = file_logging_level
        self.default_to_console = default_to_console

        if log_file_path is None:
            self.log_file_path = os.path.join(eqrm_path, 'EQRM.log')
        else:
            self.log_file_path = log_file_path
            
        self.initialise()


    def initialise(self):
        """ 
        """
        # setup the file logging system
        print "self.logger_id", self.logger_id
        self.logger = logging.getLogger(self.logger_id)
        self.logger = logging.getLogger("root")
        self.logger.setLevel(self.file_logging_level)

        self.add_console_handler()

        # catch exceptions

        #sys.excepthook = log_exception_hook

        # mark module as *setup*  Doing this after add_file_handler
        # will result in a recursive loop

        #_setup = True
        
        self.add_file_handler()  

    def add_file_handler(self):
        """ define a handler which writes to the log file
        """
        print "log_filename",self.log_file_path
        log_file_hdlr = logging.FileHandler(self.log_file_path)
        log_file_hdlr.setLevel(self.file_logging_level)
        formatter = logging.Formatter(FMT)
        log_file_hdlr.setFormatter(formatter)
        self.logger.addHandler(log_file_hdlr)


    
    def add_console_handler(self):
        """define a console handler which writes to sys.stdout
        """
    
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(self.console_logging_level)
        formatter = logging.Formatter('%(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
            
def log_exception_hook(type, value, tb):
    """Hook function to process uncaught exceptions.

    type:   Type of exception.
    value:  The exception data.
    tb:     Traceback object.

    This has the same interface as sys.excepthook().
    """

    msg = '\n' + ''.join(traceback.format_exception(type, value, tb))
    critical(msg)

if __name__ == '__main__':
    l = Log()
    l.logger.critical('now')
    print "l.log_file_path", l.log_file_path
