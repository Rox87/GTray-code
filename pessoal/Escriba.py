import logging
from logging.handlers import RotatingFileHandler
import os

class registrador:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Create file handler which logs even debug messages
        log_file = os.path.join(logs_dir, 'application.log')
        fh = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
        fh.setLevel(logging.DEBUG)

        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Remove existing handlers to prevent duplicates
        if self.logger.handlers:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

        # Add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def addHand(self):
        # No need to reinitialize since handlers are properly managed in __init__
        pass

    def get_logger(self):
        return self.logger