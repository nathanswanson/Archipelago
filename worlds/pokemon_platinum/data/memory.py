from enum import IntEnum


class PlatMemoryMap(IntEnum):
    PLAT_CONF = 0x102da0 # 64
    PLAT_BATTLE_CONF = 0x212020 # 32
    PLAT_STARTERS = 0x358ac0 # 32
