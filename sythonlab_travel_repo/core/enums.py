"""Shared enumerations used across all travel repository modules."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from enum import Enum


class Continent(Enum):
    """Geographic continents."""

    AF = "Africa"
    AS = "Asia"
    EU = "Europe"
    NA = "North America"
    OC = "Australia/Oceania"
    SA = "South America"


class FilterType(Enum):
    """Matching strategy applied to a filter field.

    EQ requires an exact (case-insensitive) match.
    CONTAINS requires the query to appear anywhere in the value.
    """

    EQ = "eq"
    CONTAINS = "contains"


class SortOrder(Enum):
    """Sort direction for query results."""

    ASC = "asc"
    DESC = "desc"


class Language(Enum):
    """Supported output languages for localized fields."""

    EN = "en"
    ES = "es"
