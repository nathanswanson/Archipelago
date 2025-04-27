import pkgutil
from os import PathLike
from typing import ClassVar, TextIO, override, Dict, Any

from BaseClasses import Tutorial
from Options import OptionGroup
import os
from worlds.AutoWorld import WebWorld, World
from .client import PokemonPlatinumClient
from .data.plat_data import PlatinumEnum
from .data.pokemon_types import PokemonPlatinumType
from worlds.pokemon_platinum.util.randomize import randomize_map_from_enum
from .data.species import Species
from .patch import PokemonPlatinumProcedurePatch
from .platinum_options import *
from .platinum_options import PokemonPlatinumRStarter, PokemonPlatinumOptions
from .platinum_settings import PokemonPlatinumSettings
from .randomizer import generate_randomize_data


class PokemonPlatinumWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "Pokémon Platinum Archipelago guide.",
        "English",
        "setup_en.md",
        "setup/en",
        ["nathan swanson"]
    )

    tutorials = [setup_en]
    options = [
        OptionGroup(
            "test", [
                PokemonPlatinumRStarter,
            ], True,
        ),
    ]




class PokemonPlatinumWorld(World):
    game = "Pokemon Platinum"
    web = PokemonPlatinumWebWorld()
    topology_present = True

    options: PokemonPlatinumOptions
    options_dataclass = PokemonPlatinumOptions
    settings: ClassVar[PokemonPlatinumSettings]

    item_name_to_id = pokemon
    item_name_to_name = {
        "test": 2
    }
    location_name_to_id = {
        "test": 2
    }
    _generated_data = {}

    @staticmethod
    def enum_map_to_string(enum: Dict[PlatinumEnum, PlatinumEnum]) -> str:
        out = "\tMAP\n"
        black_listed_out = "\tBLACKLIST\n"
        for entry in enum:
            if entry in entry.__class__.black_listed_default_values():
                black_listed_out += f"\t\t{entry} => {enum[entry]}\n"
            else:
                out += f"\t\t{entry} => {enum[entry]}\n"
        return out + black_listed_out

    def add_generated_data(self, key: str, data_map: Any):
        self._generated_data[key] = data_map
    @override
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write("Starters\n")
        spoiler_handle.writelines([f"   {Species(starter).name}\n" for starter in self._generated_data["starters"]])
        spoiler_handle.write("\n")
        if self.options.pokemon_types.value != 0:
            spoiler_handle.write("Types\n")
            spoiler_handle.write(self.enum_map_to_string(self._generated_data["type_map"]))
            spoiler_handle.write("\n")

        if self.options.wild_pokemon.value != 0:
            spoiler_handle.write("Wild Encounters\n")
            spoiler_handle.write(self.enum_map_to_string(self._generated_data["wild_map"]))
            spoiler_handle.write("\n")

    @override
    def generate_output(self, output_dir: PathLike) -> None:
        # patch the rom with the static binary
        _patch = PokemonPlatinumProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        _patch.write_file("platinum_base.bsdiff4", pkgutil.get_data(__name__, "data/platinum_base.bsdiff4"))

        # tokens
        _patch.generate_tokens(self)

        # create options file for post token patch
        _patch.write_file("randomizer.json", generate_randomize_data(self))

        # write the patch to the output directory
        rom_path = os.path.join(output_dir,
                                f"{self.multiworld.get_out_file_name_base(self.player)}{_patch.patch_file_ending}")
        _patch.write(rom_path)


