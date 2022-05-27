import re
from collections import defaultdict
from enum import Enum
from typing import Final, Optional

from pydantic import BaseModel

from collins.encode import decode_number, encode_number

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
    DELETE = "-"
    INSERT = "+"


class EncodedOperations(BaseModel):
    encoded: str = ""
    char_bank: str = ""
    delta_len: int = 0

    def __add__(self, other: "EncodedOperations") -> "EncodedOperations":
        return EncodedOperations(
            encoded=self.encoded + other.encoded,
            char_bank=self.char_bank + other.char_bank,
            delta_len=self.delta_len + other.delta_len,
        )

    def __str__(self) -> str:
        return f"{self.encoded}{OPERATION_LIST_END}{self.char_bank}"

    def __repr__(self) -> str:
        return f'EncodedOperations("{self.encoded}", "{self.char_bank}")'


class Operation:
    def __init__(
        self,
        type: OperationTypes,
        char_n: int = 0,
        line_no: int = 0,
        char_bank: str = "",
    ) -> None:
        self.type: OperationTypes = type

        """
        The number of characters to keep, insert, or delete.
        """
        self.char_n: int = char_n

        """
        The number of characters among the `chars` characters that are newlines.
        If non-zero, the last character must be a newline.
        """
        self.line_no: int = line_no

        self.char_bank = char_bank

    def invert(self) -> "Operation":
        inverted_type: OperationTypes = OperationTypes.KEEP

        if self.type == OperationTypes.INSERT:
            self.type = OperationTypes.DELETE

        if self.type == OperationTypes.DELETE:
            self.type = OperationTypes.INSERT

        self.type = inverted_type

        return self

    def append(self, another_operation: "Operation") -> None:
        """
        Appends another component to this one
        """
        if not another_operation or not another_operation.char_n:
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

        return -self.char_n if self.type == OperationTypes.DELETE else 0

    def ltrim(self, char_n: int, line_n: int) -> "Operation":
        """
        Removes N chars and L lines from the start of this component
        """
        # TODO: validate
        self.char_n -= char_n
        self.line_no -= line_n
        self.char_bank = self.char_bank[char_n:]

        return self

    def rtrim(self, char_n: int, line_n: int) -> "Operation":
        """
        Keeps N chars and L lines and trim end of this char_bank
        """
        # TODO: validate
        self.char_n = char_n
        self.line_no = line_n
        self.char_bank = self.char_bank[:char_n]

        return self

    def encode(self) -> EncodedOperations:
        return EncodedOperations(
            encoded=f"{'|' + encode_number(self.line_no) if self.line_no else ''}"
            f"{self.type}"
            f"{encode_number(self.char_n)}",
            char_bank=self.char_bank,
            delta_len=self.delta_len(),
        )

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.type == other.type
            and self.char_n == other.char_n
            and self.line_no == other.line_no
            and self.char_bank == other.char_bank
        )

    def __repr__(self) -> str:
        reps: dict[OperationTypes, str] = {
            OperationTypes.KEEP: "Keep",
            OperationTypes.DELETE: "Remove",
            OperationTypes.INSERT: "Insert",
        }

        return f'{reps[self.type]}Operation({self.char_n}:{self.line_no}, "{self.char_bank}")'

    @classmethod
    def keep(cls, char_n: int, line_no: int = 0) -> "Operation":
        return cls(
            type=OperationTypes.KEEP,
            char_n=char_n,
            line_no=line_no,
        )

    @classmethod
    def insert(cls, char_n: int, line_no: int = 0, char_bank: str = "") -> "Operation":
        return cls(
            type=OperationTypes.INSERT,
            char_n=char_n,
            line_no=line_no,
            char_bank=char_bank,
        )

    @classmethod
    def delete(cls, char_n: int, line_no: int = 0) -> "Operation":
        return cls(
            type=OperationTypes.DELETE,
            char_n=char_n,
            line_no=line_no,
        )


class OperationIterator:
    def __init__(self, operations: list[Operation]) -> None:
        self._operations = operations
        self._i: int = 0
        self._backlist = []

    def __iter__(self) -> "OperationIterator":
        self._i: int = 0
        self._backlist: list[Operation] = []

        return self

    def __next__(self) -> Operation:
        if self._i >= (len(self._operations) + len(self._backlist)):
            raise StopIteration

        item: Operation = (
            len(self._backlist) and self._backlist.pop()
        ) or self._operations[self._i]
        self._i += 1

        return item

    def append_back(self, operation: Operation) -> None:
        self._backlist.append(operation)


class OperationList:
    def __init__(self, operations: Optional[list[Operation]] = None) -> None:
        self._operations: list[Operation] = operations or []

    def append(self, operation: Operation) -> None:
        if not operation.char_n:
            return

        self._operations.append(operation)

    def extend(self, operations: list[Operation]) -> None:
        self._operations.extend(operations)

    def __iter__(self) -> OperationIterator:
        return OperationIterator(operations=self._operations)

    def __len__(self) -> int:
        return len(self._operations)

    def __getitem__(self, i: int) -> Operation:
        return self._operations[i]

    def __eq__(self, other: "OperationList") -> bool:
        if len(self) != len(other):
            return False

        return all((first == second for first, second in zip(self, other)))

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
                    registry[OperationTypes.DELETE] + registry[OperationTypes.INSERT]
                )

                registry[OperationTypes.DELETE] = []
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
            + registry[OperationTypes.DELETE]
            + registry[OperationTypes.INSERT]
            + registry[OperationTypes.KEEP]
        )

    @classmethod
    def decode(cls, encoded_operators: EncodedOperations) -> "OperationList":
        operations: list[Operation] = []
        char_bank: str = encoded_operators.char_bank

        for operator_match in re.finditer(OPERATION_REGEX, encoded_operators.encoded):
            if operator_match.group("end") == OPERATION_LIST_END:
                # Start of the insert operation character bank, so no more operations to parse
                return cls(operations)

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
                    char_bank=operation_char_bank,
                )
            )

        return cls(operations)

    @classmethod
    def decode_str(cls, encoded_operations: str, char_bank: str) -> "OperationList":
        return cls.decode(
            EncodedOperations(
                encoded=encoded_operations,
                char_bank=char_bank,
            )
        )

    """
        function flush(finalize) {
        if(buf.last.opcode) {
          if(finalize && buf.last.opcode == OpComponent.KEEP && buf.last.attribs.isEmpty()) {
            // final keep, drop
          } else {
            push(res, buf.last.pack(optPool));
            buf.last.clear();
            if(buf.inner.opcode) {
              push(res, buf.inner.pack(optPool));
              buf.inner.clear();
            }
          }
        }
      }

      function append(op) {
        if(buf.last.opcode == op.opcode && buf.last.attribs.equals(op.attribs)) {
          if(op.lines > 0) {
            // last and inner are all mergable into multi-line op
            buf.last.append(buf.inner).append(op);
            buf.inner.clear();
          } else if (buf.last.lines == 0) {
            // last and op are both in-line
            buf.last.append(op);
          } else {
            buf.inner.append(op);
          }
        } else {
          flush();
          op.copyTo(buf.last);
        }
      }
    """

    def encode(self) -> EncodedOperations:
        """
        Packs components list into compact form that can be sent over the network
         or stored in the database. Performs smart packing, specifically:
         - reorders components to keep removals before insertions
         - merges mergeable components into one
         - drops final "pure" keeps (that don't do formatting)
        """
        self.reorder()

        encoded_operations: EncodedOperations = EncodedOperations()

        last_operation: Optional[Operation] = None
        inner_operation: Optional[Operation] = None

        for operation in self._operations:
            if not last_operation or last_operation.type != operation.type:
                if last_operation:
                    encoded_operations += last_operation.encode()

                    if inner_operation:
                        encoded_operations += inner_operation.encode()
                        inner_operation = None

                last_operation = operation
                continue

            if last_operation and last_operation.type == operation.type:
                if operation.line_no:
                    # last and inner are all mergable into multi-line op
                    last_operation.append(inner_operation)
                    last_operation.append(operation)
                    inner_operation = None
                    continue

                if not last_operation.line_no:
                    # last and op are both in-line
                    last_operation.append(operation)
                    continue

                if not inner_operation:
                    inner_operation = operation
                else:
                    inner_operation.append(operation)

        # flush the last

        if not last_operation:
            return encoded_operations

        if last_operation.type == OperationTypes.KEEP:
            # drop the final keep. TODO: WHY?
            return encoded_operations

        encoded_operations += last_operation.encode()

        if inner_operation:
            encoded_operations += inner_operation.encode()

        return encoded_operations

    def append_keep(self, char_n: int, line_n: int) -> None:
        self._operations.append(Operation(OperationTypes.KEEP, char_n, line_n))

    def append_insert(self, char_n: int, line_n: int, char_bank: str) -> None:
        self._operations.append(
            Operation(OperationTypes.INSERT, char_n, line_n, char_bank)
        )

    def append_remove(self, char_n: int, line_n: int, char_bank: str) -> None:
        self._operations.append(
            Operation(OperationTypes.DELETE, char_n, line_n, char_bank)
        )

    def invert(self) -> "OperationList":
        return OperationList([operation.invert() for operation in self._operations])

    def delta_len(self) -> int:
        return sum([operation.delta_len() for operation in self._operations])

    def __repr__(self) -> str:
        return f"OperationList(operations: {len(self._operations)})"
