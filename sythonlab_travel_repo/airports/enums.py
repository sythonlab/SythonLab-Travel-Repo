from enum import Enum


class AirportType(Enum):
    MEDIUM_AIRPORT = "medium_airport"
    LARGE_AIRPORT = "large_airport"


class AirportSortField(Enum):
    ID = "id"
    NAME = "name"
    IATA_CODE = "iata_code"
    ICAO_CODE = "ident"
    COUNTRY = "iso_country"
    REGION = "iso_region"
    CITY = "municipality"
    GPS_CODE = "gps_code"
    ELEVATION = "elevation_ft"
