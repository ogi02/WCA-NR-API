# Python dependencies
from enum import Enum
from typing import Self


class ResultType(Enum):
    """
    Enumeration, representing result types of WCA records. These include - Single, Average.
    """

    SINGLE = 1
    AVERAGE = 2

    @classmethod
    def from_database_value(cls, result_type: str) -> Self:
        """
        Returns the class value of the result type.

        :param result_type: (str) The result type, accepts "SINGLE" / "AVERAGE".
        :return: (ResultType) The class value of the result type.
        """

        match result_type:
            case "SINGLE":
                return ResultType.SINGLE
            case "AVERAGE":
                return ResultType.AVERAGE
