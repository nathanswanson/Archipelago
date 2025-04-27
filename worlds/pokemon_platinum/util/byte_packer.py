from typing_extensions import TYPE_CHECKING

from worlds.Files import APTokenTypes
if TYPE_CHECKING:
    from worlds.pokemon_platinum import PokemonPlatinumProcedurePatch


class BytePacker:
    def __init__(self, data: int = 0, size_bits: int = 32):
        self.data = data
        self.size_bits = size_bits
        self.offset = 0
        assert size_bits in (8, 16, 32, 64), "size_bits must be 8, 16, 32, or 64"

    def pack(self, value: int, size_bits: int) -> bool:
        # make sure size_bits can be allocated
        if size_bits + self.offset > self.size_bits:
            return False
        # make sure value fits in size_bits
        if value >= (1 << size_bits) + 1:
            return False
        self.data |= (value << self.offset) & ((1 << self.size_bits) - 1)
        self.offset += size_bits
        return True

    def write_to_patch(self, address: int, patch: "PokemonPlatinumProcedurePatch", apt: APTokenTypes = APTokenTypes.WRITE):
        # has to write each byte separately
        for i in range(self.size_bits // 8):
            patch.write_token(apt, address + i, (self.data >> (i * 8) & 0xFF).to_bytes())

