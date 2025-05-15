# Python dependencies
import os
import shutil

# Project dependencies
from wca_nr_api.config.constants import *
from wca_nr_api.config.logger import logger


def setup_files() -> None:
    """
    Creates the following folders if they do not exist:
    database - for storing the database
    exports - for storing the WCA export files
    logs - for storing the logs
    results - for storing the results
    """

    # Database folder
    if os.path.exists(DATABASE_FOLDER):
        logger.info(f"{DATABASE_FOLDER} already exists")
    else:
        os.mkdir(DATABASE_FOLDER)
        logger.info(f"{DATABASE_FOLDER} created")
    # Exports folder
    if os.path.exists(EXPORTS_FOLDER):
        logger.info(f"{EXPORTS_FOLDER} already exists")
    else:
        os.mkdir(EXPORTS_FOLDER)
        logger.info(f"{EXPORTS_FOLDER} created")
    # Logs folder
    if os.path.exists(LOGS_FOLDER):
        logger.info(f"{LOGS_FOLDER} already exists")
    else:
        os.mkdir(LOGS_FOLDER)
        logger.info(f"{LOGS_FOLDER} created")
    # Results folder
    if os.path.exists(RECORDS_FOLDER):
        logger.info(f"{RECORDS_FOLDER} already exists")
    else:
        os.mkdir(RECORDS_FOLDER)
        logger.info(f"{RECORDS_FOLDER} created")


def clear_files() -> None:
    """
    Deletes all the contents of the export folder. Clear the database file
    """

    # Iterate through the content of the exports folder
    for filename in os.listdir(EXPORTS_FOLDER):
        # Get full path to file
        file_path = os.path.join(EXPORTS_FOLDER, filename)
        try:
            # If directory
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                logger.info(f"Deleted folder: {file_path}")
            # If file
            elif os.path.isfile(file_path) or os.path.islink(file_path):
                # Do not delete .gitkeep
                if filename == ".gitkeep":
                    continue
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Error while deleting file {filename}: {e}")

    # Delete database
    try:
        os.remove(os.path.join(DATABASE_FOLDER, DATABASE_FILENAME))
        logger.info(f"Deleted database file: {os.path.join(DATABASE_FOLDER, DATABASE_FILENAME)}")
    except Exception as e:
        logger.error(f"Error while deleting database {os.path.join(DATABASE_FOLDER, DATABASE_FILENAME)}: {e}")
