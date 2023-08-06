from struct import unpack

from .base import Packet, Opcode


class TimeRequest(Packet):
    OPCODE = Opcode.Time
    SIMPLE = True

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        time, = unpack("!I", payload)

        return {
            'time': time
        }
