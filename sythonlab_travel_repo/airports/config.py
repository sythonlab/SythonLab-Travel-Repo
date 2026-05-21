from dataclasses import dataclass

from sythonlab_travel_repo.core.enums import FilterType


@dataclass
class FilterConfig:
    icao_code: FilterType = FilterType.EQ
    name: FilterType = FilterType.EQ
    iso_country: FilterType = FilterType.EQ
    iso_region: FilterType = FilterType.EQ
    city_name: FilterType = FilterType.EQ
    gps_code: FilterType = FilterType.EQ
    iata_code: FilterType = FilterType.EQ
