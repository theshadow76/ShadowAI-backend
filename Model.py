import logging

class Text2TextModel:
    TASK = "Text2Text"
    def __init__(self, **kwargs):
        pass
    
    def setup_logger(self, level=logging.DEBUG, format=None, **kwargs):
        file = f"{self.TASK}_logs.txt"
        if format is None:
            format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=file, level=level, format=format, **kwargs)
        return logging.getLogger(self.__class__.__name__)
    
    @property
    def name(self):
        return self.__class__.__name__
