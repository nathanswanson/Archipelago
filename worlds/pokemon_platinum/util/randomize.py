import random
from typing import List, TypeVar, Type, Dict, Set

from worlds.pokemon_platinum.data.plat_data import PlatinumEnum

T = TypeVar('T', bound=PlatinumEnum)
def randomize_from_enum(enum: Type[T], black_list: List[T], count: int = 0):
    choices = []
    for i in range(count):
        choices_left = [e for e in enum if e not in black_list or e not in choices]
        choices.append(random.choice(choices_left))
    return choices

U = TypeVar('U', bound=PlatinumEnum)
def randomize_map_from_enum(enum: Type[U], black_list: Set[U] | List[U]) -> Dict[int, int]:
    values = [e for e in list(enum) if e not in black_list and e not in enum.black_listed_default_values()]
    shuffled_values = values.copy()
    random.shuffle(shuffled_values)
    rand_map = dict(zip(values, shuffled_values))
    rand_map.update(zip(black_list, black_list))
    black_list_defaults = enum.black_listed_default_values()
    rand_map.update(zip(black_list_defaults, black_list_defaults))
    return rand_map

