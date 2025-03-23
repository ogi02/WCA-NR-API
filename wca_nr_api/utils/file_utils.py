# Python dependencies
import json
import os
from typing import Any
from zipfile import ZipFile

# Project dependencies
from wca_nr_api.config.constants import *
from wca_nr_api.config.logger import logger


def unarchive_latest_export() -> None:
    """
    Unzips the results export archive.
    """

    # Get path to ZIP archive
    archive_location = os.path.join(EXPORTS_FOLDER, EXPORTS_ARCHIVE_FILENAME)
    logger.info(f"Attempting to unarchive archive stored in: {archive_location}")

    # Open archive in reading mode
    with ZipFile(archive_location, "r") as zf:
        # Extract archive
        zf.extractall(EXPORTS_FOLDER)
        zf.close()

        logger.info(f"Extracted files are stored in: {EXPORTS_FOLDER}")
        logger.info(f"Files: {[f for f in os.listdir(EXPORTS_FOLDER)]}")


def get_export_metadata() -> dict[str, Any]:
    """
    Extracts the metadata of the export, including date and version.

    :return: (dict) Dictionary with export date and export version format
    """

    # Get path to metadata file
    metadata_location = os.path.join(EXPORTS_FOLDER, EXPORTS_METADATA_FILENAME)
    logger.info(f"Attempting to extract metadata from {metadata_location}")

    # Open JSON file in reading mode and extract the metadata
    with open(metadata_location, "r") as f:
        metadata = json.load(f)
        f.close()
        logger.info(f"Extracted metadata from {metadata_location}: {metadata}")
        return metadata
