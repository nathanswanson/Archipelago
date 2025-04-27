from enum import IntEnum
from typing import List, Set, Self


class PlatinumEnum(IntEnum):
    def __init__(self, value: int):
        super().__init__(value)
    def __str__(self):
        return self.name.split("_")[1].capitalize()

    @staticmethod
    def black_listed_default_values() -> List[int]:
        return []

    @classmethod
    def user_selectable_strings(cls) -> List[str]:
        return [value.name.split("_")[1].capitalize() for value in cls if value not in cls.black_listed_default_values()]

    @classmethod
    def selected_strings_to_enum(cls, selected_strings: List[str] | Set[str]) -> List[Self]:
        return [getattr(cls, f"{cls.__name__}_{s.upper()}") for s in selected_strings if hasattr(cls, f"{cls.__name__}_{s.upper()}")]
