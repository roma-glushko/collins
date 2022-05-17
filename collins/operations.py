import re
from collections import defaultdict
from enum import Enum
from typing import Final, Optional

from collins.encode import decode_number

OPERATION_LIST_END: Final[str] = "$"
OPERATION_REGEX: Final[
    str
] = r"(?P<attributes>(?:\*[0-9a-z]+)*)(?:\|(?P<line_num>[0-9a-z]+))?(?P<type>[-+=])(?P<char_num>[0-9a-z]+)|(?P<end>.)"


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


class Operation:
    def __init__(
        self,
        type: OperationTypes,
        char_n: int = 0,
        line_no: int = 0,
        attributes: str = "",
        char_bank: str = "",
    ) -> None:
        self.type = type

        """
        The number of characters to keep, insert, or delete.
        """
        self.char_n = char_n

        """
        The number of characters among the `chars` characters that are newlines.
        If non-zero, the last character must be a newline.
        """
        self.line_no = line_no

        """
        Identifiers of attributes to apply to the text, represented as a repeated (zero or more)
        sequence of asterisk followed by a non-negative base-36 (lower-case) integer. For example,
        '*2*1o' indicates that attributes 2 and 60 apply to the text affected by the operation. The
        identifiers come from the document's attribute pool.
        """
        self.attributes = attributes

        self.char_bank = char_bank


class OperationList:
    def __init__(self, operations: Optional[list[Operation]] = None) -> None:
        self._operations: list[Operation] = operations or []

    def append(self, operation: Operation) -> None:
        if not operation.char_n:
            return

        self._operations.append(operation)

    @property
    def operations(self) -> list[Operation]:
        return self._operations

    def reorder(self) -> None:
        """
        Reorders components to keep removals before insertions. Makes sense
        in tie operations to keep result consistent across clients.
        """
        # TODO: define dirty flag to signal a need to reorder

        last_operation: Optional[Operation] = None
        operation_buffer: list[Operation] = []
        registry: dict[OperationTypes, list[Operation]] = defaultdict(list)

        for operation in self._operations:
            if (
                operation.type == OperationTypes.KEEP
                and last_operation
                and last_operation.type != OperationTypes.KEEP
            ):
                operation_buffer += (
                    registry[OperationTypes.REMOVE] + registry[OperationTypes.INSERT]
                )

                registry[OperationTypes.REMOVE] = []
                registry[OperationTypes.INSERT] = []

            if (
                operation.type != OperationTypes.KEEP
                and last_operation
                and last_operation.type == OperationTypes.KEEP
            ):
                operation_buffer += registry[OperationTypes.KEEP]
                registry[OperationTypes.KEEP] = []

            registry[operation.type].append(operation)
            last_operation = operation

        self._operations = (
            operation_buffer
            + registry[OperationTypes.REMOVE]
            + registry[OperationTypes.INSERT]
            + registry[OperationTypes.KEEP]
        )

    @classmethod
    def decode(cls, encoded_operators: str, char_bank: str) -> "OperationList":
        operations: "OperationList" = cls()

        for operator_match in re.finditer(OPERATION_REGEX, encoded_operators):
            if operator_match.group("end") == OPERATION_LIST_END:
                # Start of the insert operation character bank, so no more operations to parse
                return operations

            if operator_match.group("end"):
                pass
                # error(`invalid operation: ${ops.slice(regex.lastIndex - 1)}`);

            type: OperationTypes = operator_match.group("type")
            char_n: int = decode_number(operator_match.group("char_num"))
            operation_char_bank: str = ""

            if type != OperationTypes.KEEP:
                operation_char_bank, char_bank = char_bank[:char_n], char_bank[char_n:]

            operations.append(
                Operation(
                    type=type,
                    char_n=char_n,
                    line_no=decode_number(operator_match.group("line_num")) or 0,
                    attributes=operator_match.group("attributes"),
                    char_bank=operation_char_bank,
                )
            )

        return operations
