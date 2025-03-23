# Python dependencies
from enum import Enum
from typing import Self


class Gender(Enum):
    """
    Enumeration, representing people genders. Currently supported - Male, Female.
    """

    MALE = 1
    FEMALE = 2

    @classmethod
    def from_database_value(cls, gender: str) -> Self:
        """
        Returns the class value of the gender.

        :param gender: (str) The gender, accepts 'm' / 'f' or "MALE" / "FEMALE".
        :return: (Gender) The class value of the gender.
        """

        match gender:
            case 'm' | "MALE":
                return Gender.MALE
            case 'f' | "FEMALE":
                return Gender.FEMALE
