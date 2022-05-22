from typing import Optional

from mutators.line import LineMutator
from operations import Operation


class TextMutator:
    """
    This mutator works with lines of AStrings. It supports multiline ops and can
    efficiently patch multiline structure in place.
    """
    def __init__(self, text: list[str]) -> None:
        self.text: list[str] = text
        self._line_idx: int = 0
        self._current_line: Optional[LineMutator] = None

    @property
    def current_line(self) -> LineMutator:
        if self._current_line:
            return self._current_line

        self._current_line = LineMutator(self.text[self._line_idx] or "")

        return self._current_line

    def insert(self, operation: Operation) -> None:
        if not operation.line_no:
            self.current_line.insert(operation)
            return

        # operation.line_no > 0

    def delete(self):
        pass

    def finish(self):
        pass