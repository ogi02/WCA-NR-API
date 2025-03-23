# Python dependencies
from typing import Any, Self

# Project dependencies
from wca_nr_api.classes.event import Event
from wca_nr_api.classes.gender import Gender
from wca_nr_api.classes.result_type import ResultType
from wca_nr_api.utils.time_utils import centiseconds_to_time


class Record:
    """
    "Record" class holds the information for a single WCA national records - information about who achieved it
    (WCA ID, name, gender) and information about the event and result (event, result, result_type).
    """

    def __init__(self, person_id: str, name: str, gender: str, event: str, result: int, result_type: ResultType):
        """
        Initializer for the "Record" class.

        :param person_id: (str) The WCA ID of the person.
        :param name: (str) The name of the person.
        :param gender: (str) The gender of the person (gets automatically converted to the "Gender" enumeration).
        :param event: (str) The name of the event (gets automatically converted to the "Event" enumeration).
        :param result: (int) The result of the record.
        :param result_type: (ResultType) The type of result.
        """

        self._person_id: str = person_id
        self._name: str = name
        self._gender: Gender = Gender.from_database_value(gender)
        self._event: Event = Event.from_database_value(event)
        self._result: int = result
        self._result_type: ResultType = result_type

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def event(self) -> Event:
        return self._event

    @property
    def result(self) -> int:
        return self._result

    @property
    def result_type(self) -> ResultType:
        return self._result_type

    def validate(self) -> bool:
        """
        Validates that every field of the record has a value different from "None".

        :return: (bool) "True" if all values are valid, "False" otherwise.
        """

        return all(val is not None for val in [
            self.person_id, self.name, self.gender, self.event, self.result, self.result_type
        ])

    def readable_result(self) -> str:
        """
        Returns the result of the national record in readable format.

        Possible result formats:

        1. Default - the result is a time.
        The format of the result is centiseconds. It gets converted to the format "1:11.11".
        If the result is under a minute, the digit for the minutes is omitted.
        If the result is under 10 seconds, the digit for the minutes and the first digit for the seconds are omitted.

        2. 3x3 FMC Single - the result is a move count.
        The result is not modified at all.

        3. 3x3 FMC Mean - the result is a mean of a move count.
        The result needs to be divided by 100 in order to get the mean result.

        4. 3x3 Multiblind - the result is mathematically formulated.
        The result is a 9-digit number, which includes the points, the time and the amount of unsolved cubes.
        Example: 400346703 (The 62/65 in 57:47 WR attempt of Graham Siggins).
        The first 2 digits (40) represent the points of the attempt, when subtracted from 99. In this case - 59.
        The 3rd digit (0) is always 0 and is a divider.
        From 4th to 7th digit (3467) is the time of the attempt in seconds. In this case - 3467,
        which when converted to `minutes:seconds` becomes 57:47.
        The 8th digit (0) is always 0 and is a divider.
        The 9th digit represents the number of unsolved cubes. In this case - 3.
        From the points of the attempt and the number of unsolved cubes, we can get the number of solved and attempted:
        `solved` = `points` + `unsolved`, `attempted` = `solved` + `unsolved`. In this case `solved` = 59 + 3 = 62,
        `attempted` = 62 + 3 = 65.

        :return: (str) The result of the national record in readable format.
        """

        # Different result format for 3x3 FMC (single & average)
        if self.event == Event.THREE_X_THREE_FMC:
            if self.result_type == ResultType.SINGLE:
                return str(self.result)
            if self.result_type == ResultType.AVERAGE:
                return format(self.result / 100, ".2f")

        # Different result format for 3x3 MBF
        elif self.event == Event.THREE_X_THREE_MULTIBLIND:
            res = str(self.result)
            # Score is (99 - first two digits)
            score = 99 - int(res[:2])
            # Time is 4th digit to 7th digit including
            time = centiseconds_to_time(int(res[2:-1])*10)
            # Unsolved cubes is the last digit
            unsolved = int(res[-1])
            solved = score + unsolved
            attempted = solved + unsolved
            return f"{solved}/{attempted} - {time}"

        # Default
        else:
            return centiseconds_to_time(self.result)

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the record for storing in the records file for future use.

        :return: (dict) The record for storing in the records file.
        """

        return {
            "person_id": self.person_id,
            "name": self.name,
            "gender": self.gender.name,
            "result": self.result,
            "event": self.event.database_value(),
            "result_type": self.result_type.name
        }

    def to_readable_dict(self) -> dict[str, Any]:
        """
        Returns a readable dictionary representation of the record for printing in the console and debugging.

        :return: (dict) The record for printing in the console and debugging.
        """

        return {
            "person_id": self.person_id,
            "name": self.name,
            "gender": self.gender.name,
            "result": self.readable_result(),
            "event": self.event.readable_name(),
            "result_type": self.result_type.name
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Returns the class value from a dictionary of information for a record.

        :param data: (dict) The information for the record.
        :return: (Record) The record in a class.
        """

        return cls(
            data.get("person_id"),
            data.get("name"),
            data.get("gender"),
            data.get("event"),
            data.get("result"),
            ResultType.from_database_value(data.get("result_type"))
        )

    def __str__(self) -> str:
        """
        String representation of the record.

        :return: (str) The string representation of the record.
        """

        return str(self.to_readable_dict())

    def __eq__(self, other: Self) -> bool:
        """
        Equality check for two records.

        :param other: (Record) The other record.
        :return: (bool) True if the records are equal, False otherwise.
        """

        if isinstance(other, Record):
            return (self.person_id == other.person_id
                    and self.name == other.name
                    and self.event == other.event
                    and self.result == other.result
                    and self.result_type == other.result_type)

        return False

    def __hash__(self) -> int:
        """
        Returns the hash value of the record.

        :return: (int) The hash value of the record.
        """

        return hash((self.person_id, self.name, self.event, self.result_type, self.result))
