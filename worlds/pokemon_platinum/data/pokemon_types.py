from typing import List

from worlds.pokemon_platinum.data.plat_data import PlatinumEnum


class PokemonPlatinumType(PlatinumEnum):
    TYPE_NORMAL       =  0
    TYPE_FIGHTING     =  1
    TYPE_FLYING       =  2
    TYPE_POISON       =  3
    TYPE_GROUND       =  4
    TYPE_ROCK         =  5
    TYPE_BUG          =  6
    TYPE_GHOST        =  7
    TYPE_STEEL        =  8
    TYPE_MYSTERY      =  9
    TYPE_FIRE         = 10
    TYPE_WATER        = 11
    TYPE_GRASS        = 12
    TYPE_ELECTRIC     = 13
    TYPE_PSYCHIC      = 14
    TYPE_ICE          = 15
    TYPE_DRAGON       = 16
    TYPE_DARK         = 17
    NUM_POKEMON_TYPES = 18

    @staticmethod
    def black_listed_default_values() -> List[int]:
        return [PokemonPlatinumType.TYPE_MYSTERY, PokemonPlatinumType.NUM_POKEMON_TYPES]