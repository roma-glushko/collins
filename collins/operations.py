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
        type: Optional[OperationTypes] = None,
        char_n: int = 0,
        line_no: int = 0,
        attributes: str = "",
        char_bank: str = "",
    ) -> None:
        self.type: Optional[OperationTypes] = type

        """
        The number of characters to keep, insert, or delete.
        """
        self.char_n: int = char_n

        """
        The number of characters among the `chars` characters that are newlines.
        If non-zero, the last character must be a newline.
        """
        self.line_no: int = line_no

        """
        Identifiers of attributes to apply to the text, represented as a repeated (zero or more)
        sequence of asterisk followed by a non-negative base-36 (lower-case) integer. For example,
        '*2*1o' indicates that attributes 2 and 60 apply to the text affected by the operation. The
        identifiers come from the document's attribute pool.
        """
        self.attributes = attributes

        self.char_bank = char_bank

    def invert(self) -> None:
        if self.type == OperationTypes.INSERT:
            self.type = OperationTypes.REMOVE
            return

        if self.type == OperationTypes.REMOVE:
            self.type = OperationTypes.INSERT
            return

        # this.attribs = this.attribs.invert();

    def append(self, another_operation: "Operation") -> None:
        """
        Appends another component to this one
        """
        if not another_operation.char_n:
            # skip no-ops operations
            return

        if not self.char_n:
            self.type = another_operation.type
            # this.attribs = otherCmp.attribs.clone();
            # TODO: add the validation if char_n > 0

        self.char_n += another_operation.char_n
        self.line_no += another_operation.line_no
        self.char_bank += another_operation.char_bank

    def delta_len(self) -> int:
        if self.type == OperationTypes.INSERT:
            return self.char_n

        return -self.char_n if self.type == OperationTypes.REMOVE else 0

    def skip(self, only_if_empty: bool = False) -> None:
        if only_if_empty and self.char_n:
            return

        self.type = None

    def ltrim(self, char_n: int, line_n: int) -> None:
        """
        Removes N chars and L lines from the start of this component
        """
        # TODO: validate
        self.char_n -= char_n
        self.line_no -= line_n
        self.char_bank = self.char_bank[char_n:]

    def rtrim(self, char_n: int, line_n: int) -> None:
        """
        Keeps N chars and L lines and trim end of this component
        """
        # TODO: validate
        self.char_n = char_n
        self.line_no = line_n
        self.char_bank = self.char_bank[:char_n]


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
                    line_no=decode_number(operator_match.group("line_num"))
                    if operator_match.group("line_num")
                    else 0,
                    attributes=operator_match.group("attributes"),
                    char_bank=operation_char_bank,
                )
            )

        return operations

    def encode(self):
        """
        Packs components list into compact form that can be sent over the network
         or stored in the database. Performs smart packing, specifically:
         - reorders components to keep removals before insertions
         - merges mergeable components into one
         - drops final "pure" keeps (that don't do formatting)
        """
        self.reorder()

        last_operation: Optional[Operation] = None
        inner_operation: Optional[Operation] = None

        for operation in self._operations:
            pass

        # {self.operations}
        # {OPERATION_LIST_END}
        # {self.char_bank}

    def delta_len(self) -> int:
        return sum([operation.delta_len() for operation in self._operations])
