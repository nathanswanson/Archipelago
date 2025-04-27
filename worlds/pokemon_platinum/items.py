from typing import Dict

from BaseClasses import Item


class PokemonPlatinumItem(Item):
    def item_label_code_map(self) -> Dict[str, int]:
        var: Dict[str, int] = {"test": 2}
        return var

    def item_label_location_map(self) -> Dict[str, int]:
        var : Dict[str, int] = {"test": 2}
        return var