import logging

class Logger(logging):
    TASKS =["Text2Text", "Text2Image", "GPUManaging", "Testing"]
    DEFAULT_TASK = "Unknown"
    def __init__(self, task, level: logging.DEBUG, format: str = "%(asctime)s %(message)s"):
        file = f"{task}_logs.txt" if task in self.TASKS else f"{self.DEFAULT_TASK}_logs.txt"

        logging.basicConfig(filename=file, level=level,
                            format=format)

if __name__ == "__main__":
    logger = Logger(task="Testing")
    logger.debug("Testing")