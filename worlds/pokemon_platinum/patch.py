import json
from typing import TYPE_CHECKING, Dict

from settings import get_settings
from worlds.Files import APTokenMixin, APProcedurePatch, APPatchExtension
from .data.memory import PlatMemoryMap
from worlds.pokemon_platinum.util.randomize import randomize_from_enum
from .data.species import Species
from ndspy import rom

from .patch_utils import encounter_build
from .util.byte_packer import BytePacker

if TYPE_CHECKING:
    from . import PokemonPlatinumWorld




class PokemonPlatinumPatchExtension(APPatchExtension):
    game = "Pokemon Platinum"
    @staticmethod
    def structure_patch(caller: APProcedurePatch, rom_bytes: bytes) -> bytes:
        # create a new rom object
        plat_rom = rom.NintendoDSRom(rom_bytes)
        # options
        json_options = json.loads(caller.get_file("randomizer.json").decode())
        encounter_maps: Dict[str, Dict[str, int]] = {}
        # wild pokemon
        if json_options["wild_map"]["enabled"]:
            encounter_maps["wild_pokemon"] = json_options["wild_map"]["map"]

        if json_options["type_map"]["enabled"]:
            pass # TODO: implement type map

        if json_options["random_trainer_parties"]:
            pass # TODO: implement trainer parties
        encounter_build(plat_rom, encounter_maps)
        return plat_rom.save()


class PokemonPlatinumProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon Platinum"
    hash = "d66ad7a2a0068b5d46e0781ca4953ae9"
    patch_file_ending = ".applat"
    result_file_ending = ".nds"

    procedure = [
        ("apply_bsdiff4", ["platinum_base.bsdiff4"]),
        ("apply_tokens", ["platinum_tokens.bin"]),
        ("structure_patch", [])
    ]
    def generate_tokens(self, world: "PokemonPlatinumWorld"):
        ## STARTERS
        if world.options.starting_pokemon:
            starters = randomize_from_enum(Species, Species.selected_strings_to_enum(world.options.starter_blacklist.value), count=3)
        else:
            starters = [Species.SPECIES_TURTWIG, Species.SPECIES_CHIMCHAR, Species.SPECIES_PIPLUP]
        byte_packer_starter = BytePacker()
        byte_packer_starter.pack(starters[0], 10)
        byte_packer_starter.pack(starters[1], 10)
        byte_packer_starter.pack(starters[2], 10)
        byte_packer_starter.write_to_patch(PlatMemoryMap.PLAT_STARTERS, self)
        world.add_generated_data("starters", starters)
        ### BATTLE CONF
        # exp modifier
        byte_packer_battle = BytePacker()
        byte_packer_battle.pack(world.options.exp_modifier.value, 10)
        byte_packer_battle.pack(world.options.catch_rate.value, 1)
        byte_packer_battle.write_to_patch(PlatMemoryMap.PLAT_BATTLE_CONF, self)
        ## GENERAL AP CONF
        byte_packer_general = BytePacker()
        byte_packer_general.pack(world.options.better_shops.value, 1)
        byte_packer_general.write_to_patch(PlatMemoryMap.PLAT_CONF, self)
        self.write_file("platinum_tokens.bin", self.get_token_binary())

    @classmethod
    def get_source_data(cls) -> bytes:
        return cls._get_original_rom_bytes()

    @staticmethod
    def _get_original_rom_bytes() -> bytes:
        with open(get_settings().pokemon_platinum_options.rom_file, "rb") as f:
            file_bytes = bytes(f.read())
        return file_bytes
