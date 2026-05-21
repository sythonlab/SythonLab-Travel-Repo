import json
from pathlib import Path
from typing import Optional

from sythonlab_travel_repo.countries.config import CountryFilterConfig
from sythonlab_travel_repo.countries.enums import CountrySortField
from sythonlab_travel_repo.countries.models import Country
from sythonlab_travel_repo.core.enums import FilterType, Language, SortOrder


def _match_str(value: Optional[str], query: str, filter_type: FilterType) -> bool:
    if value is None:
        return False
    if filter_type is FilterType.CONTAINS:
        return query.lower() in value.lower()
    return value.lower() == query.lower()


class CountryService:
    _raw: list[dict] = []
    filter_config: CountryFilterConfig = CountryFilterConfig()

    @classmethod
    def load(cls):
        base_path = Path(__file__).resolve().parent
        file_path = base_path / "data" / "countries.json"

        with open(file_path, "r", encoding="utf-8") as file:
            cls._raw = json.load(file)

    @classmethod
    def configure(cls, *, filter_config: CountryFilterConfig):
        cls.filter_config = filter_config

    @classmethod
    def get_countries(
            cls,
            *,
            name: Optional[str] = None,
            nationality: Optional[str] = None,
            alpha_2: Optional[str] = None,
            alpha_3: Optional[str] = None,
            sort_by: CountrySortField = CountrySortField.NAME,
            sort_order: SortOrder = SortOrder.ASC,
            language: Language = Language.EN,
    ) -> list[Country]:
        cfg = cls.filter_config

        def matches(c: dict) -> bool:
            if name is not None:
                localized = (c.get("name") or {}).get(language.value)
                if not _match_str(localized, name, cfg.name):
                    return False
            if nationality is not None:
                nat = c.get("nationality")
                localized = (nat or {}).get(language.value) if nat else None
                if not _match_str(localized, nationality, cfg.nationality):
                    return False
            if alpha_2 is not None and not _match_str(c.get("alpha_2"), alpha_2, cfg.alpha_2):
                return False
            if alpha_3 is not None and not _match_str(c.get("alpha_3"), alpha_3, cfg.alpha_3):
                return False
            return True

        results = [c for c in cls._raw if matches(c)]

        def sort_key(c: dict):
            field = sort_by.value
            if field in ("name", "nationality"):
                val = c.get(field)
                return (val or {}).get(language.value) if val else None
            return c.get(field)

        no_value = [c for c in results if sort_key(c) is None]
        has_value = [c for c in results if sort_key(c) is not None]
        has_value.sort(key=sort_key, reverse=(sort_order is SortOrder.DESC))

        return [Country.from_dict(c) for c in has_value + no_value]

    @classmethod
    def get_by_alpha2(cls, code: str) -> Optional[Country]:
        code = code.upper()
        raw = next((c for c in cls._raw if (c.get("alpha_2") or "").upper() == code), None)
        return Country.from_dict(raw) if raw else None

    @classmethod
    def get_by_alpha3(cls, code: str) -> Optional[Country]:
        code = code.upper()
        raw = next((c for c in cls._raw if (c.get("alpha_3") or "").upper() == code), None)
        return Country.from_dict(raw) if raw else None
