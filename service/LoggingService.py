import logging
import datetime


class LoggingService(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        self.name = name
        return super(LoggingService, self).__init__(name, level)

    def default(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileName = "{0}_{1}.log".format(self.name, datetime.datetime.now().strftime("%Y-%m-%d"))
        handler = logging.FileHandler(fileName)
        handler.setFormatter(formatter)
        self.addHandler(handler)
