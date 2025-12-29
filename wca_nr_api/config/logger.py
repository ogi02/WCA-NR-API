# Python dependencies
import logging
import os
from datetime import datetime

# Project dependencies
from wca_nr_api.config.constants import LOGS_FOLDER

# Get current time for log file name
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logger_filename = os.path.join(LOGS_FOLDER, now + ".log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=logger_filename,
    encoding="utf-8",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)

# Create logger object
logger = logging.getLogger(__name__)
