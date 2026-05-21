"""AirportService for querying, filtering, and sorting airport data."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

import json
from pathlib import Path
from typing import Optional

from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.airports.enums import AirportType, AirportSortField
from sythonlab_travel_repo.airports.models import Airport
from sythonlab_travel_repo.core.enums import Continent, FilterType, SortOrder


def _match_str(field_value: Optional[str], value: str, filter_type: FilterType) -> bool:
    """Test whether a string field satisfies a query under the given filter strategy.

    Args:
        field_value: The value from the data record. Returns ``False`` if ``None``.
        value: The query string to match against.
        filter_type: ``EQ`` for exact match, ``CONTAINS`` for substring match.
            Both are case-insensitive.

    Returns:
        ``True`` if the field matches the query, ``False`` otherwise.
    """
    if field_value is None:
        return False
    if filter_type is FilterType.CONTAINS:
        return value.lower() in field_value.lower()
    return field_value.lower() == value.lower()


class AirportService:
    """Service class for loading and querying the airport dataset.

    Usage::

        AirportService.load()
        AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = AirportService.get_airports(name="Madrid")
    """

    _raw: list[dict] = []
    filter_config: FilterConfig = FilterConfig()

    @classmethod
    def load(cls) -> None:
        """Load the airport dataset from the bundled JSON file into memory."""
        base_path = Path(__file__).resolve().parent
        file_path = base_path / "data" / "airports.json"

        with open(file_path, "r", encoding="utf-8") as file:
            cls._raw = json.load(file)

    @classmethod
    def configure(cls, *, filter_config: FilterConfig) -> None:
        """Set the active filter configuration for subsequent queries.

        Args:
            filter_config: Per-field filter strategy to apply.
        """
        cls.filter_config = filter_config

    @classmethod
    def get_airports(
            cls,
            *,
            airport_id: Optional[int] = None,
            icao_code: Optional[str] = None,
            airport_type: Optional[AirportType] = None,
            name: Optional[str] = None,
            continent: Optional[Continent] = None,
            iso_country: Optional[str] = None,
            iso_region: Optional[str] = None,
            city_name: Optional[str] = None,
            gps_code: Optional[str] = None,
            iata_code: Optional[str] = None,
            sort_by: AirportSortField = AirportSortField.NAME,
            sort_order: SortOrder = SortOrder.ASC,
    ) -> list[Airport]:
        """Return airports matching all provided filters, sorted as requested.

        Only supplied parameters are used as filters; omitted ones match everything.
        String filters respect the strategy set via ``configure()``.
        Results with a ``None`` value for the sort field are placed last.

        Args:
            airport_id: Exact numeric ID.
            icao_code: ICAO code filter.
            airport_type: Airport type/size filter.
            name: Airport name filter.
            continent: Continent filter.
            iso_country: ISO country code filter.
            iso_region: ISO region code filter.
            city_name: City/municipality filter.
            gps_code: GPS code filter.
            iata_code: IATA code filter.
            sort_by: Field to sort by. Defaults to ``NAME``.
            sort_order: ``ASC`` or ``DESC``. Defaults to ``ASC``.

        Returns:
            List of matching ``Airport`` instances.
        """
        cfg: FilterConfig = cls.filter_config
        icao_code_ft: FilterType = cfg.icao_code
        name_ft: FilterType = cfg.name
        iso_country_ft: FilterType = cfg.iso_country
        iso_region_ft: FilterType = cfg.iso_region
        city_name_ft: FilterType = cfg.city_name
        gps_code_ft: FilterType = cfg.gps_code
        iata_code_ft: FilterType = cfg.iata_code

        def matches(a: dict) -> bool:
            if airport_id is not None and a.get("id") != airport_id:
                return False
            if airport_type is not None and a.get("type") != airport_type.value:
                return False
            if continent is not None and a.get("continent") != continent.name:
                return False
            if icao_code is not None and not _match_str(a.get("ident"), icao_code, icao_code_ft):
                return False
            if name is not None and not _match_str(a.get("name"), name, name_ft):
                return False
            if iso_country is not None and not _match_str(a.get("iso_country"), iso_country, iso_country_ft):
                return False
            if iso_region is not None and not _match_str(a.get("iso_region"), iso_region, iso_region_ft):
                return False
            if city_name is not None and not _match_str(a.get("municipality"), city_name, city_name_ft):
                return False
            if gps_code is not None and not _match_str(a.get("gps_code"), gps_code, gps_code_ft):
                return False
            if iata_code is not None and not _match_str(a.get("iata_code"), iata_code, iata_code_ft):
                return False
            return True

        results = [a for a in cls._raw if matches(a)]

        field = sort_by.value
        no_value = [a for a in results if a.get(field) is None]
        has_value = [a for a in results if a.get(field) is not None]
        has_value.sort(key=lambda a: a[field], reverse=(sort_order is SortOrder.DESC))

        return [Airport.from_dict(a) for a in has_value + no_value]

    @classmethod
    def get_by_iata_code(cls, code: str) -> Optional[Airport]:
        """Look up a single airport by IATA code (case-insensitive).

        Args:
            code: IATA code to search for (e.g. ``"MAD"``).

        Returns:
            The matching ``Airport``, or ``None`` if not found.
        """
        code = code.upper()
        raw = next((a for a in cls._raw if (a.get("iata_code") or "").upper() == code), None)
        return Airport.from_dict(raw) if raw else None

    @classmethod
    def get_by_icao_code(cls, code: str) -> Optional[Airport]:
        """Look up a single airport by ICAO code (case-insensitive).

        Args:
            code: ICAO code to search for (e.g. ``"LEMD"``).

        Returns:
            The matching ``Airport``, or ``None`` if not found.
        """
        code = code.upper()
        raw = next((a for a in cls._raw if (a.get("ident") or "").upper() == code), None)
        return Airport.from_dict(raw) if raw else None
