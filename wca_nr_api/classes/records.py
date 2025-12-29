# Python dependencies
from typing import Any, Self

# Project dependencies
from wca_nr_api.classes.event import Event
from wca_nr_api.classes.record import Record
from wca_nr_api.classes.result_type import ResultType
from wca_nr_api.config.constants import TABLE_PERSONS, TABLE_RANKS_AVERAGE, TABLE_RANKS_SINGLE
from wca_nr_api.config.logger import logger
from wca_nr_api.utils.database import DB


class Records:
    """
    "Records" class stores arrays of all records for all events.
    """

    def __init__(self, records: dict[str, Any] = None):
        """
        Initializer for the "Records" class.

        :param records: (dict) The records.
        """

        # If "records" are passed as an argument - assign
        # Used when extracting from storage file.
        if records:
            self._records = records

        # If "records" are not passed as an argument - initialize and extract national records
        # Used when extracting from SQL dump.
        if records is None:
            self._records = {
                "333": [],
                "222": [],
                "444": [],
                "555": [],
                "666": [],
                "777": [],
                "333bf": [],
                "333fm": [],
                "333oh": [],
                "clock": [],
                "minx": [],
                "pyram": [],
                "skewb": [],
                "sq1": [],
                "444bf": [],
                "555bf": [],
                "333mbf": []
            }
            # Extract the national records
            self.__extract_national_records_single()
            self.__extract_national_records_average()

            logger.info("Successfully initialized Records class.")

    @property
    def records(self) -> dict[str, Any]:
        return self._records

    def __extract_national_records_single(self) -> None:
        """
        Extracts the national records for all events (only Single) from the database, created from the SQL dump.
        Saves them into the respective arrays.
        """

        with DB() as database:
            # Execute SELECT query on the database
            rows = database.execute(f"SELECT p.wca_id, p.name, p.gender, rs.event_id, rs.best FROM {TABLE_RANKS_SINGLE} AS rs "
                                    f"INNER JOIN {TABLE_PERSONS} AS p "
                                    "ON rs.person_id = p.wca_id").fetchall()
            logger.info(f"Successfully executed SELECT query on `{TABLE_RANKS_SINGLE}` table.")

            # Create a "Record" class for each row and append it to the records if it is valid
            for row in rows:
                record = Record(*(row + (ResultType.SINGLE, )))
                if record.validate():
                    self.records[record.event.database_value()].append(record)
            logger.info("Created `Record` class instance for every `single` record.")

    def __extract_national_records_average(self) -> None:
        """
        Extracts the national records for all events (only Single) from the database, created from the SQL dump.
        Saves them into the respective arrays.
        """

        with DB() as database:
            # Execute SELECT query on the database
            rows = database.execute(f"SELECT p.wca_id, p.name, p.gender, ra.event_id, ra.best FROM {TABLE_RANKS_AVERAGE} AS ra "
                                    f"INNER JOIN {TABLE_PERSONS} AS p "
                                    "ON ra.person_id = p.wca_id").fetchall()
            logger.info(f"Successfully executed SELECT query on `{TABLE_RANKS_AVERAGE}` table.")

            # Create a "Record" class for each row and append it to the records if it is valid
            for row in rows:
                record = Record(*(row + (ResultType.AVERAGE, )))
                if record.validate():
                    self.records[record.event.database_value()].append(record)
            logger.info("Created `Record` class instance for every `average` record.")

    def check_for_new_records(self, old_records_class: Self) -> list[Record]:
        """
        Compares all records and returns if there are new records.

        :param old_records_class: (dict) The old records.
        :return: (list) List of new records.
        """

        all_new_records: list[Record] = []

        # Iterate all events and their records
        for event, new_records in self.records.items():
            # Get old records for this event
            old_records = old_records_class.records.get(event)

            # Obtain all records for Single
            new_records_single: list[Record] = [r for r in new_records if r.result_type == ResultType.SINGLE]
            old_records_single: list[Record] = [r for r in old_records if r.result_type == ResultType.SINGLE]

            if new_records_single and old_records_single:
                # Case 1 - New record
                if new_records_single[0].result < old_records_single[0].result:
                    all_new_records.extend(new_records_single)

                # Case 2 - Tied record
                elif len(new_records_single) > len(old_records_single):
                    diff_records = set(new_records_single) - set(old_records_single)
                    all_new_records.extend(diff_records)

            # Obtain all records for Average
            new_records_average: list[Record] = [r for r in new_records if r.result_type == ResultType.AVERAGE]
            old_records_average: list[Record] = [r for r in old_records if r.result_type == ResultType.AVERAGE]

            if new_records_average and old_records_average:
                # Case 1 - New record
                if new_records_average[0].result < old_records_average[0].result:
                    all_new_records.extend(new_records_average)

                # Case 2 - Tied record
                elif len(new_records_average) > len(old_records_average):
                    diff_records = set(new_records_average) - set(old_records_average)
                    all_new_records.extend(diff_records)

        if not all_new_records:
            logger.info("No new records found.")
        for record in all_new_records:
            logger.info(f"Extracted new NR - {record.__str__()}")

        return all_new_records

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the records by creating a dictionary representation of each record.

        :return: (dict) The dictionary representation of the records.
        """

        return {
            event: [record.to_dict() for record in records] for event, records in self.records.items()
        }

    @classmethod
    def from_dict(cls, records: dict[str, Any]) -> Self:
        """
        Returns a class instance from a dictionary representation of the records.
        Creates a "Record" class for every record in the dictionary.

        :param records: (dict) The dictionary representation of the records.
        :return: (Record) The class instance.
        """

        # For every event
        for value in records.values():
            # For every record for the respective event
            for i in range(len(value)):
                value[i] = Record.from_dict(value[i])

        return cls(records)

    def __str__(self) -> str:
        """
        Returns a string representation of the records by creating a string representation of each record.

        :return: (str) The string representation of the records.
        """

        return '\n'.join([
            f"{Event.readable_name(Event.from_database_value(event))}: {record.__str__()}"
            for event, records in self.records.items() for record in records
        ])
