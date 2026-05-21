import json
from pathlib import Path
from typing import Optional

from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.airports.enums import AirportType, AirportSortField
from sythonlab_travel_repo.airports.models import Airport
from sythonlab_travel_repo.core.enums import Continent, FilterType, SortOrder


def _match_str(field_value: Optional[str], value: str, filter_type: FilterType) -> bool:
    if field_value is None:
        return False
    if filter_type is FilterType.CONTAINS:
        return value.lower() in field_value.lower()
    return field_value.lower() == value.lower()


class AirportService:
    _raw: list[dict] = []
    filter_config: FilterConfig = FilterConfig()

    @classmethod
    def load(cls):
        base_path = Path(__file__).resolve().parent
        file_path = base_path / "data" / "airports.json"

        with open(file_path, "r", encoding="utf-8") as file:
            cls._raw = json.load(file)

    @classmethod
    def configure(cls, *, filter_config: FilterConfig):
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
        cfg = cls.filter_config

        def matches(a: dict) -> bool:
            if airport_id is not None and a.get("id") != airport_id:
                return False
            if airport_type is not None and a.get("type") != airport_type.value:
                return False
            if continent is not None and a.get("continent") != continent.name:
                return False
            if icao_code is not None and not _match_str(a.get("ident"), icao_code, cfg.icao_code):
                return False
            if name is not None and not _match_str(a.get("name"), name, cfg.name):
                return False
            if iso_country is not None and not _match_str(a.get("iso_country"), iso_country, cfg.iso_country):
                return False
            if iso_region is not None and not _match_str(a.get("iso_region"), iso_region, cfg.iso_region):
                return False
            if city_name is not None and not _match_str(a.get("municipality"), city_name, cfg.city_name):
                return False
            if gps_code is not None and not _match_str(a.get("gps_code"), gps_code, cfg.gps_code):
                return False
            if iata_code is not None and not _match_str(a.get("iata_code"), iata_code, cfg.iata_code):
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
        code = code.upper()
        raw = next((a for a in cls._raw if (a.get("iata_code") or "").upper() == code), None)
        return Airport.from_dict(raw) if raw else None

    @classmethod
    def get_by_icao_code(cls, code: str) -> Optional[Airport]:
        code = code.upper()
        raw = next((a for a in cls._raw if (a.get("ident") or "").upper() == code), None)
        return Airport.from_dict(raw) if raw else None
