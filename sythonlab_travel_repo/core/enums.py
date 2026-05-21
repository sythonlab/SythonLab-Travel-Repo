from enum import Enum


class Continent(Enum):
    AF = "Africa"
    AS = "Asia"
    EU = "Europe"
    NA = "North America"
    OC = "Australia/Oceania"
    SA = "South America"


class FilterType(Enum):
    EQ = "eq"
    CONTAINS = "contains"


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class Language(Enum):
    EN = "en"
    ES = "es"
