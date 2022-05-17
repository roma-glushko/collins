import re
from typing import Final, Match

from collins.encode import decode_number, encode_length
from collins.operations import OPERATION_LIST_END, OperationList

CHANGESET_SIGNALTURE: Final[str] = "Z:"
CHANGESET_HEADER_REGEX: Final[
    str
] = rf"{CHANGESET_SIGNALTURE}(?P<original_length>[0-9a-z]+)(?P<diff_sign>[><])(?P<new_len_diff>[0-9a-z]+)|"

"""
exports.compose = (cs1, cs2, pool) => {
  const unpacked1 = exports.unpack(cs1);
  const unpacked2 = exports.unpack(cs2);
  const len1 = unpacked1.oldLen;
  const len2 = unpacked1.newLen;
  assert(len2 === unpacked2.oldLen, 'mismatched composition of two changesets');
  const len3 = unpacked2.newLen;
  const bankIter1 = exports.stringIterator(unpacked1.charBank);
  const bankIter2 = exports.stringIterator(unpacked2.charBank);
  const bankAssem = exports.stringAssembler();

  const newOps = applyZip(unpacked1.ops, unpacked2.ops, (op1, op2) => {
    const op1code = op1.opcode;
    const op2code = op2.opcode;
    if (op1code === '+' && op2code === '-') {
      bankIter1.skip(Math.min(op1.chars, op2.chars));
    }
    const opOut = slicerZipperFunc(op1, op2, pool);
    if (opOut.opcode === '+') {
      if (op2code === '+') {
        bankAssem.append(bankIter2.take(opOut.chars));
      } else {
        bankAssem.append(bankIter1.take(opOut.chars));
      }
    }
    return opOut;
  });

  return exports.pack(len1, len3, newOps, bankAssem.toString());
};
"""


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
            new_doc_length if new_doc_length else self._calculate_new_doc_length()
        )

    def __call__(self, text: str) -> str:
        pass

    def compose(self, changeset: "ChangeSet") -> "ChangeSet":
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
            f">{encode_length(len_diff)}"
            if len_diff >= 0
            else f"<{encode_length(-len_diff)}"
        )

        return (
            f"{CHANGESET_SIGNALTURE}"
            f"{encoded_original_length}{len_diff_encoded}{self.operations}{OPERATION_LIST_END}{self.char_bank}"
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
        char_bank: str = serialized_changeset[operation_list_end + 1:]

        return cls(
            original_doc_length=original_doc_length,
            new_doc_length=new_doc_length,
            operations=OperationList.decode(serialized_operations, char_bank),
        )

    def _calculate_new_doc_length(self):
        pass
