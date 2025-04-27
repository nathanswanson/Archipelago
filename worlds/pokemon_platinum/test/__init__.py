import pkgutil
from typing import cast


from test.bases import WorldTestBase
from worlds.pokemon_platinum import PokemonPlatinumWorld


class PokemonPlatinumTestBase(WorldTestBase):
    game = "Pokemon Platinum"

    def get_world(self) -> PokemonPlatinumWorld:
        return cast(PokemonPlatinumWorld, self.multiworld.worlds[1])

    def encounter_data_integrity(self):
        classes = []
        for _, module_name, _ in pkgutil.iter_modules(__path__):
            print(module_name)
        self.assertEqual(0, 1)