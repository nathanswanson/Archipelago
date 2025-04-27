import io
import struct
from collections.abc import Buffer
from typing import List, override, Self, cast

from .serializable import Serializable


class SurfEncounterData:
    def __init__(self, level_min: int, level_max: int, species: int):
        self.level_min = level_min
        self.level_max = level_max
        self.species = species
    level_min: int
    level_max: int
    # pad 2
    species: int

class LandEncounterData:
    def __init__(self, level: int, species: int):
        self.level = level
        self.species = species
    level: int
    species: int

class EncounterData(Serializable):
    walking_rate: int
    land_encounters: list[LandEncounterData] # 12

    swarm: List[int] # 2
    morning: List[int] # 2
    night: List[int] # 2

    radar: List[int] # 4
    # pad 24
    padding_a: bytes
    ruby: List[int] # 2
    sapphire: List[int] # 2
    emerald: List[int] # 2
    fire_red: List[int] # 2
    leaf_green: List[int] # 2

    surf_rate: int
    surf_encounters: List[SurfEncounterData] # 5
    # pad 44
    padding_b: bytes
    old_rod: int
    old_rod_encounters: List[SurfEncounterData] # 5
    good_rod: int
    good_rod_encounters: List[SurfEncounterData] # 5
    super_rod: int
    super_rod_encounters: List[SurfEncounterData] # 5

    @override
    def size(self) -> int:
        return 424

    @staticmethod
    def _get_land_encounters(buffer) -> List[LandEncounterData]:
        land_encounter = []
        for _ in range(12):
            level = struct.unpack("<I", buffer.read(4))[0]
            species = struct.unpack("<I", buffer.read(4))[0]
            land_encounter.append(LandEncounterData(level, species))
        return land_encounter

    @staticmethod
    def _get_surf_encounters(buffer, size=5) -> List[SurfEncounterData]:
        surf_encounter = []
        for _ in range(size):
            min_level = struct.unpack("<B",    buffer.read(1))[0]
            max_level = struct.unpack("<B",    buffer.read(1))[0]
            # pad 2
            buffer.read(2)
            species = struct.unpack("<I", buffer.read(4))[0]
            surf_encounter.append(SurfEncounterData(min_level, max_level, species))
        return surf_encounter

    @staticmethod
    def _surf_encounter_bytes(encounter: List[SurfEncounterData]) -> bytes:
        _bytes = bytearray()
        for i in range(5):
            _bytes.extend(struct.pack("<B", encounter[i].level_min))
            _bytes.extend(struct.pack("<B", encounter[i].level_max))
            # pad 2
            _bytes.extend(b'\x00\x00')
            _bytes.extend(struct.pack("<I", encounter[i].species))
        return _bytes

    @staticmethod
    def _land_encounter_bytes(encounter: List[LandEncounterData]) -> bytes:
        _bytes = bytearray()
        for i in range(12):
            _bytes.extend(struct.pack("<I", encounter[i].level))
            _bytes.extend(struct.pack("<I", encounter[i].species))
        return _bytes

    @override
    def deserialize(self, data: bytes) -> Self:
        buffer = io.BytesIO(cast(Buffer, data))
        # Walking rate
        self.walking_rate=struct.unpack("<I", cast(Buffer, buffer.read(4)))[0]
        self.land_encounters=EncounterData._get_land_encounters(buffer)
        # Swarm
        self.swarm=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Morning
        self.morning=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Night
        self.night=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Radar
        self.radar=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(4)]
        # pad 24
        self.padding_a=buffer.read(24)
        # Ruby
        self.ruby=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Sapphire
        self.sapphire=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Emerald
        self.emerald=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Fire Red
        self.fire_red=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Leaf Green
        self.leaf_green=[struct.unpack("<I", cast(Buffer, buffer.read(4)))[0] for _ in range(2)]
        # Surf rate
        self.surf_rate=struct.unpack("<I", cast(Buffer, buffer.read(4)))[0]
        # Surf encounters
        self.surf_encounters=EncounterData._get_surf_encounters(buffer)
        # pad 44
        self.padding_b=buffer.read(44)
        # Old rod
        self.old_rod=struct.unpack("<I", cast(Buffer, buffer.read(4)))[0]
        # Old rod encounters
        self.old_rod_encounters=EncounterData._get_surf_encounters(buffer)
        # Good rod
        self.good_rod=struct.unpack("<I", cast(Buffer, buffer.read(4)))[0]
        # Good rod encounters
        self.good_rod_encounters=EncounterData._get_surf_encounters(buffer)
        # Super rod
        self.super_rod=struct.unpack("<I", cast(Buffer, buffer.read(4)))[0]
        # Super rod encounters
        self.super_rod_encounters=EncounterData._get_surf_encounters(buffer)
        assert buffer.tell() == 424, f"Encounter data size is {buffer.tell()} bytes"
        return self

    @override
    def serialize(self) -> bytes:
        encounter_bytes = io.BytesIO(cast(Buffer, bytearray()))

        # Walking rate
        encounter_bytes.write(cast(Buffer,  struct.pack("<I", self.walking_rate)))
        # Land encounters
        encounter_bytes.write(cast(Buffer, self._land_encounter_bytes(self.land_encounters)))
        # Swarm
        for swarm in self.swarm:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", swarm)))

        # Morning
        for morning in self.morning:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", morning)))

        # Night
        for night in self.night:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", night)))

        # Radar
        for radar in self.radar:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", radar)))
        # pad 24
        encounter_bytes.write(cast(Buffer, self.padding_a))

        # Ruby
        for ruby in self.ruby:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", ruby)))

        # Sapphire
        for sapphire in self.sapphire:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", sapphire)))

        # Emerald
        for emerald in self.emerald:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", emerald)))

        # Fire Red
        for fire_red in self.fire_red:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", fire_red)))

        # Leaf Green
        for leaf_green in self.leaf_green:
            encounter_bytes.write(cast(Buffer, struct.pack("<I", leaf_green)))

        # Surf rate
        encounter_bytes.write(cast(Buffer, struct.pack("<I", self.surf_rate)))
        # Surf encounters
        encounter_bytes.write(cast(Buffer, EncounterData._surf_encounter_bytes(self.surf_encounters)))

        # pad 44
        encounter_bytes.write(cast(Buffer, self.padding_b))
        # Old rod
        encounter_bytes.write(cast(Buffer, struct.pack("<I", self.old_rod)))
        # Old rod encounters
        encounter_bytes.write(cast(Buffer, EncounterData._surf_encounter_bytes(self.old_rod_encounters)))

        # Good rod
        encounter_bytes.write(cast(Buffer, struct.pack("<I", self.good_rod)))
        # Good rod encounters
        encounter_bytes.write(cast(Buffer, EncounterData._surf_encounter_bytes(self.good_rod_encounters)))
        # Super rod
        encounter_bytes.write(cast(Buffer, struct.pack("<I", self.super_rod)))
        # Super rod encounters
        encounter_bytes.write(cast(Buffer, EncounterData._surf_encounter_bytes(self.super_rod_encounters)))
        assert encounter_bytes != 424, f"Encounter data size is {encounter_bytes.tell()} bytes"
        return encounter_bytes.getvalue()