import re
from typing import Final, Match

from collins.encode import decode_number, encode_length
from collins.operations import OPERATION_LIST_END, OperationList

CHANGESET_SIGNALTURE: Final[str] = "C:"
CHANGESET_HEADER_REGEX: Final[
    str
] = rf"{CHANGESET_SIGNALTURE}(?P<original_length>[0-9a-z]+)(?P<diff_sign>[><])(?P<new_len_diff>[0-9a-z]+)|"


class ChangeSet:
    def __init__(
        self,
        original_doc_length: int,
        operations: OperationList,
        new_doc_length: int = None,
    ) -> None:
        self.operations = operations
        self.original_doc_length = original_doc_length

        self.new_doc_length = (
            new_doc_length
            if new_doc_length is not None
            else self.original_doc_length + self.operations.delta_len()
        )

    def __call__(self, text: str) -> str:
        pass

    def compose(self, changeset: "ChangeSet") -> "ChangeSet":
        """
        Compose this changeset with other changeset, producing cumulative result of both changes
        """
        pass
        # return ChangeSet(
        #     original_doc_length=self.original_doc_length,
        #     new_doc_length=changeset.new_doc_length,
        #     operations=composed_operations,
        #     char_bank=composed_bank,
        # )

    def transform(self):
        pass

    def encode(self) -> str:
        encoded_original_length: str = encode_length(self.original_doc_length)
        len_diff: int = self.new_doc_length - self.original_doc_length

        len_diff_encoded: str = (
            f"{'>' if len_diff >= 0 else '<'}" f"{encode_length(abs(len_diff))}"
        )

        enc_operations = self.operations.encode()

        return (
            f"{CHANGESET_SIGNALTURE}"
            f"{encoded_original_length}{len_diff_encoded}{enc_operations}"
        )

    @classmethod
    def decode(cls, serialized_changeset: str) -> "ChangeSet":
        header_part_matches: Match[str] = re.search(
            CHANGESET_HEADER_REGEX, serialized_changeset
        )

        if not header_part_matches:
            pass

        original_doc_length: int = decode_number(
            header_part_matches.group("original_length")
        )
        len_diff_sign: int = 1 if header_part_matches.group("diff_sign") == ">" else -1
        len_delta: int = decode_number(header_part_matches.group("new_len_diff"))

        new_doc_length: int = original_doc_length + len_diff_sign * len_delta

        header_length: int = len(header_part_matches[0])
        operation_list_end: int = serialized_changeset.find(OPERATION_LIST_END)

        serialized_operations: str = serialized_changeset[
            header_length:operation_list_end
        ]
        char_bank: str = serialized_changeset[operation_list_end + 1 :]

        return cls(
            original_doc_length=original_doc_length,
            new_doc_length=new_doc_length,
            operations=OperationList.decode(serialized_operations, char_bank),
        )
