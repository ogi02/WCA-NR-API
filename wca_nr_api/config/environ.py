# Python dependencies
import os

# External dependencies
from dotenv import load_dotenv

# Project dependencies
from wca_nr_api.config.constants import ENVIRONMENT_FOLDER, EXPECTED_ENV_VARS
from wca_nr_api.config.logger import logger

def load_environment():
    """
    Loads and validates the environmental variables.
    """

    logger.info("Started extracting environment variables.")
    load_dotenv(os.path.join(ENVIRONMENT_FOLDER, ".env"))

    # Validate environmental variables
    for expected_env_var in EXPECTED_ENV_VARS:
        if not os.environ.get(expected_env_var):
            raise Exception(f"{expected_env_var} not found in environmental file in {ENVIRONMENT_FOLDER}/.env.")
