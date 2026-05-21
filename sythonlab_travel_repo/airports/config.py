"""Filter configuration for AirportService."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from dataclasses import dataclass

from sythonlab_travel_repo.core.enums import FilterType


@dataclass
class FilterConfig:
    """Per-field filter strategy for airport queries.

    Each field controls how the corresponding parameter in
    ``AirportService.get_airports`` is matched against the data.
    Defaults to exact (case-insensitive) matching for all fields.

    Attributes:
        icao_code: Matching strategy for the ICAO code field.
        name: Matching strategy for the airport name field.
        iso_country: Matching strategy for the ISO country code field.
        iso_region: Matching strategy for the ISO region code field.
        city_name: Matching strategy for the city/municipality field.
        gps_code: Matching strategy for the GPS code field.
        iata_code: Matching strategy for the IATA code field.
    """

    icao_code: FilterType = FilterType.EQ
    name: FilterType = FilterType.EQ
    iso_country: FilterType = FilterType.EQ
    iso_region: FilterType = FilterType.EQ
    city_name: FilterType = FilterType.EQ
    gps_code: FilterType = FilterType.EQ
    iata_code: FilterType = FilterType.EQ
