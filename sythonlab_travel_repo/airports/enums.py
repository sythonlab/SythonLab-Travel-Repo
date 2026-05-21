"""Airport-specific enumerations."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from enum import Enum


class AirportType(Enum):
    """Airport size/traffic classification."""

    MEDIUM_AIRPORT = "medium_airport"
    LARGE_AIRPORT = "large_airport"


class AirportSortField(Enum):
    """Fields available for sorting airport query results."""

    ID = "id"
    NAME = "name"
    IATA_CODE = "iata_code"
    ICAO_CODE = "ident"
    COUNTRY = "iso_country"
    REGION = "iso_region"
    CITY = "municipality"
    GPS_CODE = "gps_code"
    ELEVATION = "elevation_ft"
