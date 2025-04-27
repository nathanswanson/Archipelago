import json

from typing_extensions import TYPE_CHECKING

from worlds.pokemon_platinum.data.pokemon_types import PokemonPlatinumType
from worlds.pokemon_platinum.util.randomize import randomize_map_from_enum
from worlds.pokemon_platinum.data.species import Species

if TYPE_CHECKING:
    from worlds.pokemon_platinum import PokemonPlatinumWorld


def generate_randomize_data(world: "PokemonPlatinumWorld") -> bytes:
    randomizer_json = {
        "type_map": {
            "enabled": world.options.pokemon_types != 0,
            "map": {}
        },
        "wild_map": {
            "enabled": world.options.wild_pokemon != 0,
            "map": {}
        },
        "random_trainer_parties":
            world.options.trainer_party.value,
        "random_trainer_items":
        {
            "enabled": world.options.trainer_items.value,
            "map": {}
        }

    }

    if world.options.pokemon_types != 0:
        type_map = randomize_map_from_enum(PokemonPlatinumType, PokemonPlatinumType.selected_strings_to_enum(
            world.options.types_blacklist.value))
        randomizer_json["type_map"]["map"] = type_map
        world.add_generated_data("type_map", type_map)

    if world.options.wild_pokemon != 0:
        wild_map = randomize_map_from_enum(Species, Species.selected_strings_to_enum(
            world.options.wild_pokemon_blacklist.value
        ))
        randomizer_json["wild_map"]["map"] = wild_map
        world.add_generated_data("wild_map", wild_map)
    return json.dumps(randomizer_json).encode()

