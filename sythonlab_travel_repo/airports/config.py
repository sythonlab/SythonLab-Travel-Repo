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
        country_name: Matching strategy for the localized country name field.
    """

    icao_code: FilterType = FilterType.CONTAINS
    name: FilterType = FilterType.CONTAINS
    iso_country: FilterType = FilterType.CONTAINS
    iso_region: FilterType = FilterType.CONTAINS
    city_name: FilterType = FilterType.CONTAINS
    gps_code: FilterType = FilterType.CONTAINS
    iata_code: FilterType = FilterType.CONTAINS
    country_name: FilterType = FilterType.CONTAINS
