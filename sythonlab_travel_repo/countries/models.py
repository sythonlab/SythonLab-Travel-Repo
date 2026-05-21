from dataclasses import dataclass, field
from typing import Optional

from sythonlab_travel_repo.core.enums import Language


@dataclass
class LocalizedText:
    en: str
    es: str

    def __str__(self) -> str:
        return f"{self.en} / {self.es}"

    def get(self, language: Language) -> str:
        return self.en if language is Language.EN else self.es


@dataclass
class Country:
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
