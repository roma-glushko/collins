import re
from contextlib import suppress
from copy import deepcopy
from typing import TYPE_CHECKING, Callable, Final, List, Match, Optional

from collins.encode import decode_number, encode_number
from collins.mutators.text import TextMutator
from collins.operations import (
    OPERATION_LIST_END,
    EncodedOperations,
    Operation,
    OperationIterator,
    OperationList,
    OperationTypes,
)

if TYPE_CHECKING:
    from collins.document import Document

SIGNATURE: Final[str] = "C:"
HEADER_REGEX: Final[
    str
] = rf"{SIGNATURE}(?P<original_length>[0-9a-z]+)(?P<diff_sign>[><])(?P<new_len_diff>[0-9a-z]+)|"

SplitFunc = Callable[[Operation, Operation], bool]


class ParallelOperationIterator:
    def __init__(
        self,
        first_ops: OperationList,
        second_ops: OperationList,
        splitter: SplitFunc,
    ) -> None:
        self.first_ops = first_ops
        self.second_ops = second_ops
        self.splitter = splitter

    def __iter__(self) -> "ParallelOperationIterator":
        self.first_iterator: OperationIterator = iter(self.first_ops)
        self.second_iterator: OperationIterator = iter(self.second_ops)

        self._first_backlist: List[Operation] = []
        self._second_backlist: List[Operation] = []

        self.first_part: Optional[Operation] = None
        self.second_part: Optional[Operation] = None

        return self

    def __next__(self) -> tuple[Optional[Operation], Optional[Operation]]:
        next_first: Optional[Operation] = None
        next_second: Optional[Operation] = None

        with suppress(StopIteration):
            next_first = len(self._first_backlist) and self._first_backlist.pop()

            if not next_first:
                next_first = self.first_part
                self.first_part = None

            if not next_first:
                next_first = next(self.first_iterator)

        with suppress(StopIteration):
            next_second = len(self._second_backlist) and self._second_backlist.pop()

            if not next_second:
                next_second = self.second_part
                self.second_part = None

            if not next_second:
                next_second = next(self.second_iterator)

        if not next_first and not next_second:
            raise StopIteration()

        if next_first and next_second:
            # pre-splitting into equal slices greatly reduces
            # number of code branches and makes code easier to read
            need_splitting: bool = self.splitter(next_first, next_second)

            if not need_splitting:
                return next_first, next_second

            if next_first.char_n > next_second.char_n:
                self.first_part = deepcopy(next_first).ltrim(
                    next_second.char_n, next_second.line_no
                )
                next_first.rtrim(next_second.char_n, next_second.line_no)

            if next_first.char_n < next_second.char_n:
                self.second_part = deepcopy(next_second).ltrim(
                    next_first.char_n, next_first.line_no
                )
                next_second.rtrim(next_first.char_n, next_first.line_no)

        return next_first, next_second

    def append_first_back(self, operation: Operation) -> None:
        self._first_backlist.append(operation)

    def append_second_back(self, operation: Operation) -> None:
        self._second_backlist.append(operation)


class Changeset:
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

    def __call__(self, document: "Document") -> "Document":
        """
        Apply changeset to the document, modifying it in-place.
        """
        text_mutator: TextMutator = document.mutate()
        self.operations.reorder()

        for operation in self.operations:
            # if we reuse (don't pack) changeset object, we can end up with
            # empty operations sometimes, do not process them.
            if not operation.char_n:
                continue

            if operation.type == OperationTypes.INSERT:
                text_mutator.insert(operation)

            if operation.type == OperationTypes.DELETE:
                """
                Since we can have multiline remove ops, remove() can
                return an array of components instead of single one.
                But since they all should be mergeable, we can run a quick
                reduce operation and compare the result
                """
                text_mutator.delete(operation)

            if operation.type == OperationTypes.KEEP:
                text_mutator.skip(operation)

        text_mutator.finish()

        return document

    def compose(self, changeset: "Changeset") -> "Changeset":
        """
        Compose this changeset with other changeset, producing cumulative result of both changes
        """

        def splitter(first_op: Operation, second_op: Operation) -> bool:
            no_split: bool = (
                first_op.type == OperationTypes.DELETE
                or second_op.type == OperationTypes.INSERT
            )

            # KEEPS can be replaced by DELETEs
            has_keep: bool = (
                first_op.type == OperationTypes.KEEP
                or second_op.type == OperationTypes.KEEP
            )

            # REMOVEs can affect KEEPs and INSERTs but not other DELETEs
            has_remove_actual: bool = (first_op.type != second_op.type) and (
                first_op.type == OperationTypes.DELETE
                or second_op.type == OperationTypes.DELETE
            )

            return (has_keep or has_remove_actual) and not no_split

        self.operations.reorder()
        changeset.operations.reorder()

        operation_iterator: ParallelOperationIterator = ParallelOperationIterator(
            first_ops=self.operations,
            second_ops=changeset.operations,
            splitter=splitter,
        )

        composed_operations: list[Operation] = []

        for first_operation, second_operation in iter(operation_iterator):
            if (
                first_operation and first_operation.type == OperationTypes.DELETE
            ) or not second_operation:
                # if we've removed something, it cannot be undone by next op
                composed_operations.append(first_operation)
                operation_iterator.append_second_back(second_operation)
                continue

            if (
                second_operation and second_operation.type == OperationTypes.INSERT
            ) or not first_operation:
                # if other is inserting something it should be inserted
                composed_operations.append(second_operation)
                operation_iterator.append_first_back(first_operation)
                continue

            if second_operation and second_operation.type == OperationTypes.DELETE:
                # at this point we're operating on actual chars (KEEP or INSERT) in the target string
                # we don't validate KEEPs since they just add format and not keep final attributes list

                # delete_valid: bool = \
                #  first_operation.type == OperationTypes.KEEP or first_operation == second_operation
                # TODO: assert

                # if there was no insert on our side, just keep the other op,
                # otherwise we're removing what was inserted and will skip both
                if first_operation and first_operation.type == OperationTypes.KEEP:
                    # undo format changes made by first_operation and compose with second_operation
                    composed_operations.append(second_operation)
                    continue

            if second_operation.type == OperationTypes.KEEP:
                # here, thisOp is also KEEP or INSERT, so just copy it over and compose with second_operation
                composed_operations.append(first_operation)

        return Changeset(
            original_doc_length=self.original_doc_length,
            new_doc_length=changeset.new_doc_length,
            operations=OperationList(composed_operations),
        )

    def invert(self) -> "Changeset":
        inverted_operations = self.operations.invert()

        return Changeset(
            original_doc_length=self.original_doc_length,
            new_doc_length=self.new_doc_length,
            operations=inverted_operations,
        )

    def transform(self, first_op: Operation, second_op: Operation) -> "Changeset":
        """
        Transform this changeset against other changeset.

        explanation for side = [left | right]
        let's say we have thisOp coming to server after otherOp,
        both creating a "tie" situation.
        server has [otherOp, thisOp]
        for server otherOp is already written, so it transforms thisOp
        by otherOp, taking otherOp as first-win and thisOp as second.
        In [otherOp, thisOp] list otherOp is on the "left"

        Server sends its otherOp back to the client, but client already
        applied thisOp operation, so his queue looks like
        [thisOp, otherOp]
        Client should transorm otherOp, and to get same results as server,
        this time it should take otherOp as first-win. In the list
        otherOp is to the "right"
        """
        pass

    def encode(self) -> str:
        enc_operations = self.operations.encode()

        encoded_original_length: str = encode_number(self.original_doc_length)
        encoded_len_diff: str = (
            f"{'>' if enc_operations.delta_len >= 0 else '<'}"
            f"{encode_number(abs(enc_operations.delta_len))}"
        )

        return (
            f"{SIGNATURE}"
            f"{encoded_original_length}{encoded_len_diff}{str(enc_operations)}"
        )

    @classmethod
    def decode(cls, serialized_changeset: str) -> "Changeset":
        header_part_matches: Match[str] = re.search(HEADER_REGEX, serialized_changeset)

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

        if operation_list_end < 0:
            operation_list_end = len(serialized_changeset)

        encoded_operations: str = serialized_changeset[header_length:operation_list_end]
        char_bank: str = serialized_changeset[operation_list_end + 1 :]

        return cls(
            original_doc_length=original_doc_length,
            new_doc_length=new_doc_length,
            operations=OperationList.decode(
                EncodedOperations(
                    encoded=encoded_operations,
                    char_bank=char_bank,
                )
            ),
        )
