import string
from enum import Enum
from typing import Final, Match

import re
from pydantic import BaseModel

LENGTH_ENCODE_BASE: Final[int] = 36
CHANGESET_SIGNALTURE: Final[str] = "Z:"
CHANGESET_HEADER_REGEX: Final[
    str] = rf"{CHANGESET_SIGNALTURE}(?P<original_length>[0-9a-z]+)(?P<diff_sign>[><])(?P<new_len_diff>[0-9a-z]+)|"
OPERATION_LIST_END: Final[str] = "$"


def decode_length(serialized_length: str) -> int:
    return int(serialized_length, LENGTH_ENCODE_BASE)


def encode_length(length: int, base: int = LENGTH_ENCODE_BASE) -> str:
    digs = string.digits + string.ascii_lowercase
    encoded: str = ""

    while length:
        encoded = digs[length % base] + encoded
        length //= base

    return encoded


class OperationTypes(str, Enum):
    """
    Types:
    - "=": Keep the next `chars` characters (containing `lines` newlines) from the base document
    - "-": Remove the next `chars` characters (containing `lines` newlines) from the base document
    - "+": Insert `chars` characters (containing `lines` newlines) at the current position in the document.
            The inserted characters come from the changeset's character bank.
    """
    KEEP = "="
    REMOVE = "-"
    INSERT = "+"


class Operation(BaseModel):
    type: OperationTypes
    char_num: int = 0
    """
    The number of characters to keep, insert, or delete.
    """

    lines: int = 0
    """
    The number of characters among the `chars` characters that are newlines.
    If non-zero, the last character must be a newline.
    """

    attribs: str = ''
    """
    Identifiers of attributes to apply to the text, represented as a repeated (zero or more)
    sequence of asterisk followed by a non-negative base-36 (lower-case) integer. For example,
    '*2*1o' indicates that attributes 2 and 60 apply to the text affected by the operation. The
    identifiers come from the document's attribute pool.
    """


class ChangeSet(BaseModel):
    original_doc_length: int
    new_doc_length: int
    operations: str
    char_bank: str

    def encode(self) -> str:
        encoded_original_length: str = encode_length(self.original_doc_length)
        len_diff: int = self.new_doc_length - self.original_doc_length
        len_diff_encoded: str = f">{encode_length(len_diff)}" if len_diff >= 0 else f"<{encode_length(-len_diff)}"

        return f"{CHANGESET_SIGNALTURE}{encoded_original_length}{len_diff_encoded}{self.operations}{OPERATION_LIST_END}{self.char_bank}"

    @classmethod
    def decode(cls, serialized_changeset: str) -> "ChangeSet":
        header_part_matches: Match[str] = re.search(CHANGESET_HEADER_REGEX, serialized_changeset)

        if not header_part_matches:
            pass

        original_doc_length: int = decode_length(header_part_matches.group("original_length"))
        len_diff_sigh: int = 1 if header_part_matches.group("diff_sign") == ">" else -1
        len_diff: int = decode_length(header_part_matches.group("new_len_diff"))

        new_doc_length: int = original_doc_length + len_diff_sigh * len_diff

        header_length: int = len(header_part_matches[0])
        operation_list_end: int = serialized_changeset.find(OPERATION_LIST_END)

        return cls(**{
            "original_doc_length": original_doc_length,
            "new_doc_length": new_doc_length,
            "operations": serialized_changeset[header_length:operation_list_end],
            "char_bank": serialized_changeset[operation_list_end + 1:],
        })
