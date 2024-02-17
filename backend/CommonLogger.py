import datetime
import os
from loguru import logger

class CommonLogger():
    def __init__(self, log_to_terminal = True): #TODO: write description
        CommonLogger.log_to_terminal = log_to_terminal
        CommonLogger.start_logs()
        CommonLogger.logger = logger

    @staticmethod
    def start_logs(self): #TODO: write description
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/logs/"
        time_now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        os.makedirs(dir_path, exist_ok=True)
        if not self.log_to_terminal:
            self.logger.remove()
        log_file_path = os.path.join(dir_path, f"log_{time_now}.log")
        self.logger.add(log_file_path, format="{time:HH:mm:ss} {level} {message}", level="DEBUG")