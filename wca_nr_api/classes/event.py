# Python dependencies
from enum import Enum
from typing import Self


class Event(Enum):
    """
    Enumeration, representing the current WCA Events.

    These include:
    3x3, 2x2, 4x4, 5x5, 6x6, 7x7,
    3x3 Blindfolded, 3x3 FMC, 3x3 one-handed,
    Clock, Megaminx, Pyraminx, Skewb, Square 1,
    4x4 Blindfolded, 5x5 Blindfolded, 3x3 Multiblind.
    """

    THREE_X_THREE = 1
    TWO_X_TWO = 2
    FOUR_X_FOUR = 3
    FIVE_X_FIVE = 4
    SIX_X_SIX = 5
    SEVEN_X_SEVEN = 6
    THREE_X_THREE_BLINDFOLDED = 7
    THREE_X_THREE_FMC = 8
    THREE_X_THREE_ONE_HANDED = 9
    CLOCK = 10
    MEGAMINX = 11
    PYRAMINX = 12
    SKEWB = 13
    SQUARE_1 = 14
    FOUR_X_FOUR_BLINDFOLDED = 15
    FIVE_X_FIVE_BLINDFOLDED = 16
    THREE_X_THREE_MULTIBLIND = 17

    __readable = {
        1: "3x3",
        2: "2x2",
        3: "4x4",
        4: "5x5",
        5: "6x6",
        6: "7x7",
        7: "3x3 Blindfolded",
        8: "3x3 FMC",
        9: "3x3 OH",
        10: "Clock",
        11: "Megaminx",
        12: "Pyraminx",
        13: "Skewb",
        14: "Square 1",
        15: "4x4 Blindfolded",
        16: "5x5 Blindfolded",
        17: "3x3 Multiblind"
    }

    def readable_name(self) -> str:
        """
        Returns the readable name of the event.

        :return: (str) The name of the event.
        """

        return self.__readable.get(self.value, "Unknown Event")

    __database_value = {
        1: "333",
        2: "222",
        3: "444",
        4: "555",
        5: "666",
        6: "777",
        7: "333bf",
        8: "333fm",
        9: "333oh",
        10: "clock",
        11: "minx",
        12: "pyram",
        13: "skewb",
        14: "sq1",
        15: "444bf",
        16: "555bf",
        17: "333mbf",
    }

    def database_value(self) -> str:
        """
        Returns the database value of the event.

        :return: (str) The database value of the event.
        """

        return self.__database_value.get(self.value, "Unknown Event")

    __from_database_value = {
        "333": 1,
        "222": 2,
        "444": 3,
        "555": 4,
        "666": 5,
        "777": 6,
        "333bf": 7,
        "333fm": 8,
        "333oh": 9,
        "clock": 10,
        "minx": 11,
        "pyram": 12,
        "skewb": 13,
        "sq1": 14,
        "444bf": 15,
        "555bf": 16,
        "333mbf": 17
    }

    @classmethod
    def from_database_value(cls, event: str) -> Self:
        """
        Returns the class value of the event based on its database value.

        :param event: (str) The database value of the event.
        :return: (Event) The class value of the event.
        """

        try:
            # This statement is in a try/except block, as there are removed WCA events in the database dump
            # and there is no need to store them, as new records for those events is impossible.
            return Event(cls.__from_database_value.get(event))
        except ValueError:
            pass
