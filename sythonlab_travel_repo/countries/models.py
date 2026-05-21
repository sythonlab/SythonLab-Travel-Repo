"""Country domain models."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from dataclasses import dataclass, field
from typing import Optional

from sythonlab_travel_repo.core.enums import Language


@dataclass
class LocalizedText:
    """A text value available in English and Spanish.

    Attributes:
        en: English text.
        es: Spanish text.
    """

    en: str
    es: str

    def __str__(self) -> str:
        return f"{self.en} / {self.es}"

    def get(self, language: Language) -> str:
        """Return the text in the requested language.

        Args:
            language: Target language.

        Returns:
            The English text for ``Language.EN``, Spanish for ``Language.ES``.
        """
        return self.en if language is Language.EN else self.es


@dataclass
class Country:
    """Represents a country with localized name and nationality.

    Attributes:
        id: Internal numeric identifier.
        name: Country name in English and Spanish.
        alpha_2: ISO 3166-1 alpha-2 code (e.g. ``ES``).
        alpha_3: ISO 3166-1 alpha-3 code (e.g. ``ESP``).
        flag: Flag emoji (e.g. ``🇪🇸``).
        nationality: Demonym in English and Spanish, or ``None`` if unavailable.
        locale: Display language used by ``__str__``. Not included in equality checks.
    """

    id: int
    name: LocalizedText
    alpha_2: str
    alpha_3: str
    flag: str
    nationality: Optional[LocalizedText]
    locale: Language = field(default=Language.EN, compare=False)

    def __str__(self) -> str:
        return self.name.get(self.locale)

    @classmethod
    def from_dict(cls, data: dict) -> "Country":
        """Construct a Country from a raw JSON record.

        Args:
            data: Dictionary as loaded from the countries JSON file.

        Returns:
            A fully populated Country instance.
        """
        name = data["name"]
        nat: Optional[dict] = data.get("nationality")
        return cls(
            id=data["id"],
            name=LocalizedText(en=name["en"], es=name["es"]),
            alpha_2=data["alpha_2"],
            alpha_3=data["alpha_3"],
            flag=data.get("flag", ""),
            nationality=LocalizedText(en=nat["en"], es=nat["es"]) if nat is not None else None,
        )
