# Python dependencies
import os
import json
from typing import Any, Self

# Project dependencies
from wca_nr_api.classes.records import Records
from wca_nr_api.config.constants import RECORDS_FOLDER, RECORDS_FILENAME

class Storage:
    """
    "Storage" class is used for storing the records in a file for later use.
    """

    def __init__(self, metadata: dict[str, Any] = None, records: Records = None):
        """
        Initializer for the "Storage" class.

        :param metadata: (dict) The metadata of the WCA export.
        :param records: (Records) The records to store.
        """

        self._metadata = metadata
        self._records = records

    @property
    def metadata(self):
        return self._metadata

    @property
    def records(self):
        return self._records

    def validate(self) -> bool:
        """
        Validates the both metadata and records are present and contain values.

        :return: (bool) "True" if storage is valid, "False" otherwise.
        """

        return self.metadata is not None and self.records is not None and sum(len(r) for r in self.records.records) > 0

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the class by creating a dictionary representation of the results.

        :return: (dict) The dictionary representation of the "Storage" class.
        """

        return {
            "metadata": self.metadata,
            "records": self.records.to_dict()
        }

    def to_json(self) -> None:
        """
        Returns a JSON representation of the class by creating a dictionary representation of the class.
        """

        with open(os.path.join(RECORDS_FOLDER, RECORDS_FILENAME), 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_json(cls) -> Self:
        """
        Creates a "Storage" class instance from a JSON representation by creating a "Records" class from the JSON data.
        :return:
        """

        with open(os.path.join(RECORDS_FOLDER, RECORDS_FILENAME), 'r') as f:
            data = json.load(f)
        return cls(data.get("metadata"), Records.from_dict(data.get("records")))
