import string
from typing import Final

LENGTH_ENCODE_BASE: Final[int] = 36


def decode_number(serialized_length: str) -> int:
    return int(serialized_length, LENGTH_ENCODE_BASE)


def encode_number(value: int, base: int = LENGTH_ENCODE_BASE) -> str:
    digs: str = string.digits + string.ascii_lowercase
    encoded: str = ""

    if value == 0:
        return str(value)

    while value:
        encoded = digs[value % base] + encoded
        value //= base

    return encoded
