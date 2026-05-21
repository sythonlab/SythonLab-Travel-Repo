"""CountryService for querying, filtering, and sorting country data."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

import json
from pathlib import Path
from typing import Any, Optional

from sythonlab_travel_repo.countries.config import CountryFilterConfig
from sythonlab_travel_repo.countries.enums import CountrySortField
from sythonlab_travel_repo.countries.models import Country
from sythonlab_travel_repo.core.enums import FilterType, Language, SortOrder
from sythonlab_travel_repo.core.utils import match_str


class CountryService:
    """Service class for loading and querying the country dataset.

    Usage::

        CountryService.load()
        CountryService.configure(
            filter_config=CountryFilterConfig(name=FilterType.CONTAINS),
            locale=Language.ES,
        )
        results = CountryService.get_countries(name="rep")
    """

    _raw: list[dict] = []
    filter_config: CountryFilterConfig = CountryFilterConfig()
    locale: Language = Language.EN

    @classmethod
    def load(cls) -> None:
        """Load the country dataset from the bundled JSON file into memory."""
        base_path = Path(__file__).resolve().parent
        file_path = base_path / "data" / "countries.json"

        with open(file_path, "r", encoding="utf-8") as file:
            cls._raw = json.load(file)

    @classmethod
    def configure(
            cls,
            *,
            filter_config: CountryFilterConfig = CountryFilterConfig(),
            locale: Language = Language.EN,
    ) -> None:
        """Set the active filter configuration and display locale for subsequent queries.

        Args:
            filter_config: Per-field filter strategy to apply.
            locale: Language used for localized filtering, sorting, and ``__str__``.
        """
        cls.filter_config = filter_config
        cls.locale = locale

    @classmethod
    def _build(cls, raw: dict) -> Country:
        """Construct a Country from a raw record and apply the current locale.

        Args:
            raw: Dictionary as loaded from the countries JSON file.

        Returns:
            A Country instance with its locale set to ``cls.locale``.
        """
        country = Country.from_dict(raw)
        country.locale = cls.locale
        return country

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
    ) -> list[Country]:
        """Return countries matching any of the provided filters, sorted as requested.

        Only supplied parameters are used as filters; omitted ones match everything.
        If multiple filters are provided, a country is included if it matches at least one (OR logic).
        String filters respect the strategy set via ``configure()``.
        Localized fields (name, nationality) are matched in the active locale.
        Results with a ``None`` value for the sort field are placed last.

        Args:
            name: Country name filter (matched in the active locale).
            nationality: Nationality/demonym filter (matched in the active locale).
            alpha_2: ISO 3166-1 alpha-2 code filter.
            alpha_3: ISO 3166-1 alpha-3 code filter.
            sort_by: Field to sort by. Defaults to ``NAME``.
            sort_order: ``ASC`` or ``DESC``. Defaults to ``ASC``.

        Returns:
            List of matching ``Country`` instances with locale applied.
        """
        cfg: CountryFilterConfig = cls.filter_config
        lang = cls.locale.value
        name_ft: FilterType = cfg.name
        nationality_ft: FilterType = cfg.nationality
        alpha_2_ft: FilterType = cfg.alpha_2
        alpha_3_ft: FilterType = cfg.alpha_3

        if not cls._raw:
            cls.load()

        def matches(c: dict) -> bool:
            conditions = []
            if name is not None:
                localized = (c.get("name") or {}).get(lang)
                conditions.append(match_str(localized, name, name_ft))
            if nationality is not None:
                nat = c.get("nationality")
                localized = (nat or {}).get(lang) if nat else None
                conditions.append(match_str(localized, nationality, nationality_ft))
            if alpha_2 is not None:
                conditions.append(match_str(c.get("alpha_2"), alpha_2, alpha_2_ft))
            if alpha_3 is not None:
                conditions.append(match_str(c.get("alpha_3"), alpha_3, alpha_3_ft))
            return any(conditions) if conditions else True

        results = [c for c in cls._raw if matches(c)]

        def sort_key(c: dict) -> Any:
            field = sort_by.value
            if field in ("name", "nationality"):
                val = c.get(field)
                return (val or {}).get(lang) if val else None
            return c.get(field)

        no_value = [c for c in results if sort_key(c) is None]
        has_value = [c for c in results if sort_key(c) is not None]
        has_value.sort(key=sort_key, reverse=(sort_order is SortOrder.DESC))

        return [cls._build(c) for c in has_value + no_value]

    @classmethod
    def search(
            cls,
            query: str,
            *,
            sort_by: CountrySortField = CountrySortField.NAME,
            sort_order: SortOrder = SortOrder.ASC,
    ) -> list[Country]:
        """Return countries where any text field contains the query string.

        Searches across: name (EN + ES), nationality (EN + ES), alpha-2, and alpha-3.
        Case-insensitive.

        Args:
            query: Text to look for in any field.
            sort_by: Field to sort by. Defaults to ``NAME``.
            sort_order: ``ASC`` or ``DESC``. Defaults to ``ASC``.

        Returns:
            List of matching ``Country`` instances with locale applied.
        """
        if not cls._raw:
            cls.load()

        q = query.lower()

        def matches(c: dict) -> bool:
            name = c.get("name") or {}
            nat = c.get("nationality") or {}
            candidates = [
                name.get("en"),
                name.get("es"),
                nat.get("en"),
                nat.get("es"),
                c.get("alpha_2"),
                c.get("alpha_3"),
            ]
            return any(q in v.lower() for v in candidates if v)

        results = [c for c in cls._raw if matches(c)]

        def sort_key(c: dict):
            field = sort_by.value
            if field in ("name", "nationality"):
                val = c.get(field)
                lang = cls.locale.value
                return (val or {}).get(lang) if val else None
            return c.get(field)

        no_value = [c for c in results if sort_key(c) is None]
        has_value = [c for c in results if sort_key(c) is not None]
        has_value.sort(key=sort_key, reverse=(sort_order is SortOrder.DESC))

        return [cls._build(c) for c in has_value + no_value]

    @classmethod
    def get_by_alpha2(cls, code: str) -> Optional[Country]:
        """Look up a single country by ISO 3166-1 alpha-2 code (case-insensitive).

        Args:
            code: Alpha-2 code to search for (e.g. ``"ES"``).

        Returns:
            The matching ``Country`` with locale applied, or ``None`` if not found.
        """
        code = code.upper()
        raw = next((c for c in cls._raw if (c.get("alpha_2") or "").upper() == code), None)
        return cls._build(raw) if raw else None

    @classmethod
    def get_by_alpha3(cls, code: str) -> Optional[Country]:
        """Look up a single country by ISO 3166-1 alpha-3 code (case-insensitive).

        Args:
            code: Alpha-3 code to search for (e.g. ``"ESP"``).

        Returns:
            The matching ``Country`` with locale applied, or ``None`` if not found.
        """
        code = code.upper()
        raw = next((c for c in cls._raw if (c.get("alpha_3") or "").upper() == code), None)
        return cls._build(raw) if raw else None
