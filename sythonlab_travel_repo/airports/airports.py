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
from sythonlab_travel_repo.core.utils import match_str


class AirportService:
    """Service class for loading and querying the airport dataset.

    Usage::

        AirportService.load()
        AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = AirportService.get_airports(name="Madrid")
    """

    _raw: list[dict] = []
    _country_index: dict[str, dict] = {}
    filter_config: FilterConfig = FilterConfig()

    @classmethod
    def load(cls) -> None:
        """Load the airport dataset from the bundled JSON file into memory."""
        base_path = Path(__file__).resolve().parent
        file_path = base_path / "data" / "airports.json"

        with open(file_path, "r", encoding="utf-8") as file:
            cls._raw = json.load(file)

        cls._load_country_index()

    @classmethod
    def _load_country_index(cls) -> None:
        """Build a lookup dict of country raw data keyed by alpha-2 code."""
        countries_path = Path(__file__).resolve().parent.parent / "countries" / "data" / "countries.json"
        with open(countries_path, "r", encoding="utf-8") as f:
            cls._country_index = {c["alpha_2"]: c for c in json.load(f)}

    @classmethod
    def _enrich(cls, raw: dict) -> dict:
        """Add ``country_name`` and ``country_flag`` to a raw airport dict."""
        if not cls._country_index:
            cls._load_country_index()
        alpha2 = raw.get("iso_country")
        if alpha2:
            country = cls._country_index.get(alpha2)
            if country:
                return {**raw, "country_name": country.get("name"), "country_flag": country.get("flag")}
        return raw

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
            country_name: Optional[str] = None,
            iso_region: Optional[str] = None,
            city_name: Optional[str] = None,
            gps_code: Optional[str] = None,
            iata_code: Optional[str] = None,
            sort_by: AirportSortField = AirportSortField.NAME,
            sort_order: SortOrder = SortOrder.ASC,
    ) -> list[Airport]:
        """Return airports matching any of the provided filters, sorted as requested.

        Only supplied parameters are used as filters; omitted ones match everything.
        If multiple filters are provided, an airport is included if it matches at least one (OR logic).
        String filters respect the strategy set via ``configure()``.
        Results with a ``None`` value for the sort field are placed last.

        Args:
            airport_id: Exact numeric ID.
            icao_code: ICAO code filter.
            airport_type: Airport type/size filter.
            name: Airport name filter.
            continent: Continent filter.
            iso_country: ISO 3166-1 alpha-2 country code filter (e.g. ``"ES"``).
            country_name: Country name filter matched against both EN and ES names.
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
        country_name_ft: FilterType = cfg.country_name
        iso_region_ft: FilterType = cfg.iso_region
        city_name_ft: FilterType = cfg.city_name
        gps_code_ft: FilterType = cfg.gps_code
        iata_code_ft: FilterType = cfg.iata_code

        if not cls._raw:
            cls.load()

        def matches(a: dict) -> bool:
            conditions = []
            if airport_id is not None:
                conditions.append(a.get("id") == airport_id)
            if airport_type is not None:
                conditions.append(a.get("type") == airport_type.value)
            if continent is not None:
                conditions.append(a.get("continent") == continent.name)
            if icao_code is not None:
                conditions.append(match_str(a.get("ident"), icao_code, icao_code_ft))
            if name is not None:
                conditions.append(match_str(a.get("name"), name, name_ft))
            if iso_country is not None:
                conditions.append(match_str(a.get("iso_country"), iso_country, iso_country_ft))
            if country_name is not None:
                c = cls._country_index.get(a.get("iso_country") or "")
                names = c.get("name") or {} if c else {}
                conditions.append(
                    match_str(names.get("en"), country_name, country_name_ft)
                    or match_str(names.get("es"), country_name, country_name_ft)
                )
            if iso_region is not None:
                conditions.append(match_str(a.get("iso_region"), iso_region, iso_region_ft))
            if city_name is not None:
                conditions.append(match_str(a.get("municipality"), city_name, city_name_ft))
            if gps_code is not None:
                conditions.append(match_str(a.get("gps_code"), gps_code, gps_code_ft))
            if iata_code is not None:
                conditions.append(match_str(a.get("iata_code"), iata_code, iata_code_ft))
            return any(conditions) if conditions else True

        results = [a for a in cls._raw if matches(a)]

        field = sort_by.value
        no_value = [a for a in results if a.get(field) is None]
        has_value = [a for a in results if a.get(field) is not None]
        has_value.sort(key=lambda a: a[field], reverse=(sort_order is SortOrder.DESC))

        return [Airport.from_dict(cls._enrich(a)) for a in has_value + no_value]

    @classmethod
    def search(
            cls,
            query: str,
            *,
            sort_by: AirportSortField = AirportSortField.NAME,
            sort_order: SortOrder = SortOrder.ASC,
    ) -> list[Airport]:
        """Return airports where any text field contains the query string.

        Searches across: ICAO code, name, country, region, city, GPS code,
        IATA code, airport type, and continent. Case-insensitive.

        Args:
            query: Text to look for in any field.
            sort_by: Field to sort by. Defaults to ``NAME``.
            sort_order: ``ASC`` or ``DESC``. Defaults to ``ASC``.

        Returns:
            List of matching ``Airport`` instances.
        """
        if not cls._raw:
            cls.load()

        q = query.lower()

        def matches(a: dict) -> bool:
            c = cls._country_index.get(a.get("iso_country") or "")
            country_names = c.get("name") or {} if c else {}
            candidates = [
                a.get("ident"),
                a.get("name"),
                a.get("iso_country"),
                a.get("iso_region"),
                a.get("municipality"),
                a.get("gps_code"),
                a.get("iata_code"),
                a.get("type"),
                a.get("continent"),
                country_names.get("en"),
                country_names.get("es"),
            ]
            return any(q in v.lower() for v in candidates if v)

        results = [a for a in cls._raw if matches(a)]

        field = sort_by.value
        no_value = [a for a in results if a.get(field) is None]
        has_value = [a for a in results if a.get(field) is not None]
        has_value.sort(key=lambda a: a[field], reverse=(sort_order is SortOrder.DESC))

        return [Airport.from_dict(cls._enrich(a)) for a in has_value + no_value]

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
        return Airport.from_dict(cls._enrich(raw)) if raw else None

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
        return Airport.from_dict(cls._enrich(raw)) if raw else None
