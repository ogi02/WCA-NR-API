# Python dependencies
import os.path
from datetime import datetime

# External dependencies
import requests
from urllib.request import urlretrieve

# Project dependencies
from wca_nr_api.config.constants import *
from wca_nr_api.config.logger import logger


class WCAUtils:
    """
    Utilities class for all requests and methods related to downloading the WCA export from the WCA website.
    """

    EXPORTS_URL = "https://www.worldcubeassociation.org/api/v0/export/public"

    def __init__(self):
        """
        Initializer for the "WCAUtils" class.
        """

        self._export_date = None
        self._sql_url = None
        self._tsv_url = None

    @property
    def export_date(self):
        return self._export_date

    @export_date.setter
    def export_date(self, date):
        self._export_date = date

    @property
    def sql_url(self):
        return self._sql_url

    @sql_url.setter
    def sql_url(self, url):
        self._sql_url = url

    @property
    def tsv_url(self):
        return self._tsv_url

    @tsv_url.setter
    def tsv_url(self, url):
        self._tsv_url = url

    def extract_latest_export_information(self) -> None:
        """
        Extracts the latest export information from the API including
        export date, SQL formatted export and TSV formatted export

        :return: None
        """

        try:
            logger.info(f"Sending GET request to {self.EXPORTS_URL}")
            # GET latest WCA export information
            response = requests.get(self.EXPORTS_URL)
            # Raise error if 4**
            response.raise_for_status()
            logger.info(f"Received response from {self.EXPORTS_URL} with status code {response.status_code}")

            # Convert response to JSON
            export_info = response.json()
            # Save export information
            self.export_date = export_info["export_date"]
            self.sql_url = export_info["sql_url"]
            self.tsv_url = export_info["tsv_url"]

            # Validate that export information is saved
            if not self.export_date or not self.sql_url or not self.tsv_url:
                logger.warning("No export information received from WCA")
            else:
                logger.info(f"Export information received from WCA and saved")
        except requests.exceptions.HTTPError as err:
            logger.error(f"Received response from {self.EXPORTS_URL} with status code {err.response.status_code}")
            logger.error(f"Error - {err.response.text}")

    def is_new_export_present(self, old_export_date: str) -> bool:
        """
        Compares the date between the export date, collected in the last script execution
        and the export date, collected in the current script execution.

        :param old_export_date: (str) The export date of the last script execution
        :return: (bool) True (if there is new export) or False (if there is no new export)
        """

        new_export_datetime = datetime.strptime(self.export_date, "%Y-%m-%dT%H:%M:%SZ")
        old_export_datetime = datetime.strptime(old_export_date, "%Y-%m-%d %H:%M:%S %Z")
        return new_export_datetime != old_export_datetime

    def download_latest_export(self) -> None:
        """
        Downloads the latest export from the API including competitors, competitions, events, results, records, etc.
        
        :return: None
        """

        # Define path and filename for archive download
        archive_download_location = os.path.join(EXPORTS_FOLDER, EXPORTS_ARCHIVE_FILENAME)
        logger.info(f"Archive download location: {archive_download_location}")

        try:
            # Send request to retrieve the exports file and save it to the specified path
            logger.info(f"Sending GET request to {self.sql_url}")
            urlretrieve(self.sql_url, filename=archive_download_location)
        except Exception as e:
            logger.error(f"Received response from {self.sql_url} with error {e}")
