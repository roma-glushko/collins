from typing import Optional

from collins.mutators.line import LineMutator
from collins.operations import EncodedOperations, Operation, OperationList


class TextMutator:
    """
    This mutator works with lines of AStrings.
    It supports multiline ops and can efficiently patch multiline structure in place.
    """

    def __init__(self, lines: list[EncodedOperations]) -> None:
        self.lines: list[EncodedOperations] = lines  # TODO: come up with a better name
        self._line_idx: int = 0
        self._current_line: Optional[LineMutator] = None

    def __iter__(self) -> "TextMutator":
        self._line_idx: int = 0
        self._current_line: Optional[LineMutator] = None

        return self

    def __next__(self) -> LineMutator:
        self._close_current_line()
        self._line_idx += 1

        return self.current_line

    def __len__(self) -> int:
        text_len: int = 0

        for idx, line in enumerate(self.lines):
            if idx == self._line_idx:
                # the line could be modified, so we need its actual size
                text_len += len(self.current_line)
                continue

            text_len += len(line.char_bank)

        return text_len

    @property
    def current_line(self) -> LineMutator:
        if self._current_line:
            return self._current_line

        self._current_line = LineMutator(
            self.lines[self._line_idx] or EncodedOperations()
        )

        return self._current_line

    @property
    def remaining_lines(self) -> int:
        """
        Number of remaining lines in the document, including current line
        """
        return len(self.lines) - self._line_idx

    def insert(self, operation: Operation) -> "TextMutator":
        if not operation.line_no:
            self.current_line.insert(operation)
            return self

        # operation.line_no > 0

        return self

    def delete(self, operation: Operation) -> "TextMutator":
        # TODO: Implement

        return self

    def skip(self, operation) -> "TextMutator":
        if not operation.line_no:
            self.current_line.skip(operation.char_n)
            return self

        self._skip_lines(operation.line_no)
        # TODO: assert

        return self

    def take(self, char_n: int, line_no: int) -> OperationList:
        if not line_no:
            return self.current_line.take(char_n)

        operations = self._take_lines(line_no)

        return operations

    def _skip_lines(self, line_no: int):
        # we do some checks here, so do first skip manually
        # TODO: assert

        char_n: int = 0

        if self.current_line:
            char_n += self.current_line.remaining()
            self._next_line()
            line_no -= 1

        # unlike _takeLines(), we do not parse each next line, just take the length

        return char_n

    def _close_current_line(self) -> None:
        if not self._current_line:
            return

        """
        fix for case with inserting into empty document - we must store first line that doesn't
        exists in collection yet
        """
        self.lines[self._line_idx] = self.current_line.finish()
        self._current_line = None

    def finish(self) -> list[EncodedOperations]:
        # make sure mutated line is finished
        self._close_current_line()

        # reset everything
        self._line_idx = 0
        return self.lines
