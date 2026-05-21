"""Filter configuration for CountryService."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from dataclasses import dataclass

from sythonlab_travel_repo.core.enums import FilterType


@dataclass
class CountryFilterConfig:
    """Per-field filter strategy for country queries.

    Each field controls how the corresponding parameter in
    ``CountryService.get_countries`` is matched against the data.
    Defaults to exact (case-insensitive) matching for all fields.

    Attributes:
        name: Matching strategy for the country name field.
        nationality: Matching strategy for the nationality field.
        alpha_2: Matching strategy for the ISO 3166-1 alpha-2 code field.
        alpha_3: Matching strategy for the ISO 3166-1 alpha-3 code field.
    """

    name: FilterType = FilterType.CONTAINS
    nationality: FilterType = FilterType.CONTAINS
    alpha_2: FilterType = FilterType.CONTAINS
    alpha_3: FilterType = FilterType.CONTAINS
