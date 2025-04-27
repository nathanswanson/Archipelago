import io
from typing import Type, Dict

from ndspy import rom

from worlds.pokemon_platinum.util.narc import BasicNarc
from worlds.pokemon_platinum.serializable.encounter_data import EncounterData, LandEncounterData
from worlds.pokemon_platinum.serializable.serializable import Serializable

ENCOUNTER_FILE = 330
TRAINER_DATA_FILE = 439
TRAINER_POKEMON_FILE = 440

def _feed(data: bytearray, serialize_type: Type[Serializable]):
    # noinspection PyTypeChecker
    buffer = io.BytesIO(data)
    chunks = []

    while True:
        serialize_obj = serialize_type()
        chunk = buffer.read(serialize_obj.size())
        if not chunk or len(chunk) < serialize_obj.size():
            break
        chunks.append(serialize_obj.deserialize(chunk))
    return chunks

def encounter_build(plat_rom: rom.NintendoDSRom, maps: Dict[str, Dict[str,int]]) -> None:
    encounter_narc = bytearray(plat_rom.files[ENCOUNTER_FILE])
    encounter_narc_content = BasicNarc(encounter_narc)
    encounters = _feed(encounter_narc_content.get_data(), EncounterData)
    for encounter in encounters:
        encounter: EncounterData
        for land_encounter in encounter.land_encounters:
            land_encounter: LandEncounterData
            if land_encounter.species == 0:
                continue
            land_encounter.species = maps["wild_pokemon"][f"{land_encounter.species}"]
    encounter_narc_content.set_list(encounters)
    plat_rom.files[ENCOUNTER_FILE] = encounter_narc_content.get_file()