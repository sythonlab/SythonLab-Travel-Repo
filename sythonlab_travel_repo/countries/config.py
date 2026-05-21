from dataclasses import dataclass

from sythonlab_travel_repo.core.enums import FilterType


@dataclass
class CountryFilterConfig:
    name: FilterType = FilterType.EQ
    nationality: FilterType = FilterType.EQ
    alpha_2: FilterType = FilterType.EQ
    alpha_3: FilterType = FilterType.EQ
