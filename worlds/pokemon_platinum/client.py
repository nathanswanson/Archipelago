from typing import TYPE_CHECKING

# noinspection PyProtectedMember
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from .._bizhawk.context import BizHawkClientContext


class PokemonPlatinumClient(BizHawkClient):
    game = "Pokemon Platinum"
    system = "NDS"
    patch_suffix = ".applat"

    def initialize_client(self) -> None:
        pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        pass

    async def validate_rom(self, ctx) -> bool:
        # header = 0x504F4B454D4F4E20504C0000435055
        return True