# Python dependencies
import os
import shutil

# Project dependencies
from wca_nr_api.classes.records import Records
from wca_nr_api.config.config import clear_files, setup_files
from wca_nr_api.config.constants import *
from wca_nr_api.config.environ import load_environment
from wca_nr_api.config.logger import logger
from wca_nr_api.utils.database import execute_sql_script
from wca_nr_api.utils.discord import send_record_announcement
from wca_nr_api.utils.file_utils import get_export_metadata, unarchive_latest_export
from wca_nr_api.utils.mail import send_email
from wca_nr_api.utils.sql_utils import filter_sql_dump
from wca_nr_api.utils.storage import Storage
from wca_nr_api.utils.wca_utils import WCAUtils


def extract_last_known_records() -> Storage:
    """
    Retrieves the last known records and metadata from the storage file.

    :return: (Storage) An instance of the Storage class with metadata and all records.
    """

    # Extract old metadata and records
    logger.info(f"Started extracting last known records from {os.path.join(RECORDS_FOLDER, RECORDS_FILENAME)}")
    storage = Storage.from_json()
    logger.info(f"Successfully extracted last known records from {os.path.join(RECORDS_FOLDER, RECORDS_FILENAME)}")

    # Validate storage
    if not storage.validate():
        raise Exception("Last known metadata and storage are not valid!")

    return storage


def download_latest_wca_export(old_metadata_timestamp: str) -> bool:
    """
    Retrieves the latest export information from the WCA website, checks if a new export is available, downloads the
    new export and unarchives it.

    :param old_metadata_timestamp: (str) The timestamp of the last known export.
    :return: "True" if there was new export, "False" otherwise.
    """

    # Define WCA utilities class
    wca_utils = WCAUtils()

    # Extract latest export information from WCA website
    wca_utils.extract_latest_export_information()

    # Check if a new export is present (based on the saved metadata timestamp)
    if wca_utils.is_new_export_present(old_metadata_timestamp):
        logger.info("New export is available!")

        # Download the latest export
        wca_utils.download_latest_export()

        # Unarchive the latest export
        unarchive_latest_export()

        return True

    return False


def create_records_database() -> None:
    """
    Filters the SQL dump based on the configured filters.
    """

    filter_sql_dump(TABLE_FILTERS)
    execute_sql_script()


def extract_new_metadata_and_records() -> Storage:
    """
    Extracts the new metadata and records based on the new WCA export and SQL dump.

    :return: (Storage) An instance of the Storage class with metadata and records.
    """

    metadata = get_export_metadata()
    records = Records()
    return Storage(metadata, records)


if __name__ == '__main__':
    logger.info("Starting WCA NR API!")

    try:
        # Load and validate environmental variables
        load_environment()

        # Setup files and folders
        setup_files()

        # Extract last known records from storage
        old_storage = extract_last_known_records()

        # Check and download latest export from WCA
        if not download_latest_wca_export(old_storage.metadata.get("export_date")):
            logger.info("No new export is available!")

        else:
            # Verify export format version
            if get_export_metadata().get("export_format_version") != old_storage.metadata.get("export_format_version"):
                raise ValueError("Different export format version. Revisit.")

            # Create records database
            create_records_database()

            # Extract new metadata and records
            new_storage = extract_new_metadata_and_records()

            # Check for new records
            new_records = new_storage.records.check_for_new_records(old_storage.records)

            # Announce new records in Discord
            for nr in new_records:
                send_record_announcement(nr)

            # Save new storage to file
            new_storage.to_json()
            logger.info(f"Saved new version of records to {os.path.join(RECORDS_FOLDER, RECORDS_FILENAME)}")

            # Keep a backup of the records file if there are new records
            if new_records:
                # Source
                source = os.path.join(RECORDS_FOLDER, RECORDS_FILENAME)
                # Destination
                backup_date = new_storage.metadata.get("export_date").split(' ')[0]
                destination = os.path.join(BACKUP_FOLDER, BACKUP_FILENAME.format(date=backup_date))
                # Make a backup
                shutil.copyfile(source, destination, follow_symlinks=False)
                logger.info(f"Saved backup of new records to {destination}")

            # Clear files and folders
            clear_files()

        success = True
    except Exception as e:
        logger.error(e)
        success = False

    logger.info("Finished WCA NR API!")

    # Send email
    send_email(success)
