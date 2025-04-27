import io
import struct
from collections.abc import Buffer
from typing import override, cast, List

from .serializable import Serializable


class TrainerData(Serializable):
    flags: int  # 1
    trainer_class: int  # 1
    unknown: int  # 1
    party_count: int  # 1
    items: List[int]  # 2 * 4
    ai_flag: int  # 4
    double_battle: int  # 4
    def size(self) -> int:
        return 20

    @override
    def serialize(self) -> bytes:
        buf = io.BytesIO(cast(Buffer, bytes()))
        buf.write(cast(Buffer, struct.pack("<B", self.flags)))
        buf.write(cast(Buffer, struct.pack("<B", self.trainer_class)))
        buf.write(cast(Buffer, struct.pack("<B", self.unknown)))
        buf.write(cast(Buffer, struct.pack("<B", self.party_count)))
        for item in self.items:
            buf.write(cast(Buffer, struct.pack("<H", item)))
        buf.write(cast(Buffer, struct.pack("<I", self.ai_flag)))
        buf.write(cast(Buffer, struct.pack("<I", self.double_battle)))
        return buf.getvalue()

    @override
    def deserialize(self, data: bytes):
        buf = io.BytesIO(cast(Buffer, data))
        self.flags = struct.unpack("<B", (cast(Buffer, buf.read(1))))[0]
        self.trainer_class = struct.unpack("<B", (cast(Buffer, buf.read(1))))[0]
        self.unknown = struct.unpack("<B", (cast(Buffer, buf.read(1))))[0]
        self.party_count = struct.unpack("<B", (cast(Buffer, buf.read(1))))[0]
        self.items = [struct.unpack ("<H", (cast(Buffer, buf.read(2))))[0] for _ in range(4)]
        self.ai_flag = struct.unpack("<I", (cast(Buffer, buf.read(4))))[0]
        self.double_battle = struct.unpack("<I", (cast(Buffer, buf.read(4))))[0]
