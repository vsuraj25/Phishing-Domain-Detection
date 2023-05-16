import logging
from datetime import datetime
import os

## --------------------Logger--------------------------

LOG_DIR = "logs"

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode='w',
                    format='[%(asctime)s] %(name)s - %(levelname)s %(message)s',
                    level=logging.INFO
                    )

logger = logging.getLogger('phishing_predictor_logger')


## ----------------Data Validation Exception--------------------
class DataNotValid(Exception):
    def __init__(self, message = "Data is not valid"):
        self.message = message
        super().__init__(self.message)
