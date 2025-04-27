import settings

pokemon_platinum_hash = "d66ad7a2a0068b5d46e0781ca4953ae9"

class PokemonPlatinumSettings(settings.Group):
    class PokemonPlatinumROMFile(settings.UserFilePath):
        name = "Pokemon Platinum ROM"
        description = "Pokemon Platinum ROM File"
        copy_to = "pokeplatinum.us.nds"
        md5s = ["d66ad7a2a0068b5d46e0781ca4953ae9"]

    rom_file: PokemonPlatinumROMFile = PokemonPlatinumROMFile(PokemonPlatinumROMFile.copy_to)