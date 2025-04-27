from collections.abc import Buffer
from typing import List, cast

from worlds.pokemon_platinum.serializable.serializable import Serializable


class BasicNarc:
    def __init__(self, narc_file: bytearray):
        header_split = narc_file.find(cast(Buffer, "GMIF".encode("ascii")))
        self.narc_header: bytearray = narc_file[:header_split+8]
        self.narc_data: bytearray = narc_file[header_split+8:]

    def get_file(self) -> bytearray:
        return self.narc_header + cast(Buffer, self.narc_data)

    def get_data(self) -> bytearray:

        return self.narc_data

    def set_data(self, data: bytearray):
        self.narc_data = data

    def set_list(self, data: List[Serializable]):
        self.narc_data = bytearray()
        for chunk in data:
            self.narc_data.extend(chunk.serialize())