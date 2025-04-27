from dataclasses import dataclass

from Options import Choice, Toggle, PerGameCommonOptions, Range, OptionSet
from worlds.pokemon_platinum.data.pokemon_items import PokemonItems
from worlds.pokemon_platinum.data.species import Species


class PokemonPlatinumRStarter(Toggle):
    """
    Randomize starting pokemon.
    """
    display_name = "Randomize Starting Pokemon"

class PokemonPlatinumStarterBlacklist(OptionSet):
    """
    Blacklisted pokemon when randomizing starters.
    """
    display_name = "Starter Blacklist"
    valid_keys = Species.user_selectable_strings()

class PokemonPlatinumRWildPokemon(Choice):
    """
    Randomize wild pokemon.
    """
    display_name = "Randomize Wild Pokemon"
    option_normal = 0
    option_full_random = 1

class PokemonPlatinumWildBlacklist(OptionSet):
    """
    Blacklisted pokemon when randomizing wild pokemon.
    """
    display_name = "Wild Pokemon Blacklist"
    valid_keys = Species.user_selectable_strings()

class PokemonPlatinumRTrainerParty(Choice):
    """
    Randomize pokemon in trainer parties.
    """
    display_name = "Randomize Trainer Party"
    option_normal = 0
    option_match = 1
    option_full_random = 2

class PokemonPlatinumTrainerBlacklist(OptionSet):
    """
    Blacklisted pokemon when randomizing trainer parties.
    """
    display_name = "Trainer Party Blacklist"
    valid_keys = Species.user_selectable_strings()

class PokemonPlatinumRTypes(Choice):
    """
    Randomize Types between pokemon can also choose to have evolutions match types.
    """
    display_name = "Randomize Types"
    option_normal = 0
    option_shuffle = 1
    option_full_random = 2

class PokemonPlatinumTypesBlacklist(OptionSet):
    """
    Blacklisted types when randomizing types.
    """
    display_name = "Types Blacklist"
    valid_keys = Species.user_selectable_strings()

class PokemonPlatinumRTrainerItems(Toggle):
    """
    Randomize items held by trainers.
    """
    display_name = "Randomize Trainer Items"

class PokemonPlatinumRTrainerItemsBlacklist(OptionSet):
    """
    Blacklisted items when randomizing trainer items.
    """
    display_name = "Trainer Items Blacklist"
    valid_keys = PokemonItems.user_selectable_strings()

class PokemonPlatinumExpModifier(Range):
    """
    Exp multiplier 100 = 1x, 50 = 0.5x, 200 = 2x
    """
    display_name = "Exp Modifier"
    range_start = 1
    default = 100
    range_end = 1000

class PokemonPlatinumGuaranteeCatch(Toggle):
    """
    100% catch rate for all pokemon/Pokeballs
    """
    display_name = "Guarantee Catch"

class PokemonPlatinumBetterShops(Toggle):
    """
    Unlock later shop items earlier
    """
    display_name = "Better shops"

@dataclass
class PokemonPlatinumOptions(PerGameCommonOptions):
    starting_pokemon: PokemonPlatinumRStarter
    starter_blacklist: PokemonPlatinumStarterBlacklist
    wild_pokemon: PokemonPlatinumRWildPokemon
    wild_pokemon_blacklist: PokemonPlatinumWildBlacklist
    trainer_party: PokemonPlatinumRTrainerParty
    trainer_party_blacklist: PokemonPlatinumTrainerBlacklist
    pokemon_types: PokemonPlatinumRTypes
    types_blacklist: PokemonPlatinumTypesBlacklist
    trainer_items: PokemonPlatinumRTrainerItems
    trainer_items_blacklist: PokemonPlatinumRTrainerItemsBlacklist
    exp_modifier: PokemonPlatinumExpModifier
    catch_rate: PokemonPlatinumGuaranteeCatch
    better_shops: PokemonPlatinumBetterShops
