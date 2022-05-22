from operations import Operation, OperationList


class LineMutator:
    def __init__(self, line: str) -> None:
        self._line: str = line

        self._char_idx: int = 0
        self._length: int = len(self._line)

        self._position: int = 0
        self._mutated: bool = False
        self._has_new_line_char = self._line.rfind("\n") >= 0

        self._operation_history = OperationList()

    def __len__(self) -> int:
        return self._length

    @property
    def position(self) -> int:
        return self._position

    def insert(self, operation: Operation) -> None:
        self._mutated = True

        self._operation_history.append(operation)

        self._length += operation.char_n
        self._char_idx += operation.char_n