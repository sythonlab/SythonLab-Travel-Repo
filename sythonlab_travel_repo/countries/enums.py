"""Country-specific enumerations."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from enum import Enum


class CountrySortField(Enum):
    """Fields available for sorting country query results."""

    ID = "id"
    NAME = "name"
    ALPHA_2 = "alpha_2"
    ALPHA_3 = "alpha_3"
    NATIONALITY = "nationality"
