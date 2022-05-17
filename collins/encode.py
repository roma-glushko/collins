import string
from typing import Final

LENGTH_ENCODE_BASE: Final[int] = 36


def decode_number(serialized_length: str) -> int:
    return int(serialized_length, LENGTH_ENCODE_BASE)


def encode_length(length: int, base: int = LENGTH_ENCODE_BASE) -> str:
    digs = string.digits + string.ascii_lowercase
    encoded: str = ""

    while length:
        encoded = digs[length % base] + encoded
        length //= base

    return encoded
