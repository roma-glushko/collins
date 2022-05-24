from copy import deepcopy
from typing import Optional

from operations import EncodedOperations, Operation, OperationIterator, OperationList

# TODO: terrible code below. Needs some refactoring


class LineMutator:
    def __init__(self, encoded_operations: EncodedOperations) -> None:
        self._operations = OperationList.decode(encoded_operations)
        self._operation_iterator: OperationIterator = iter(self._operations)

        char_bank: str = encoded_operations.char_bank

        self._length: int = len(char_bank)
        self._current_operation: Optional[Operation] = None
        self._operation_position: int = 0

        self._mutated: bool = False
        self._has_new_line = char_bank.rfind("\n") >= 0

        self._inserted_operations = OperationList()

    def __len__(self) -> int:
        return self._length

    @property
    def mutated(self) -> bool:
        return self._mutated

    @property
    def remaining(self) -> int:
        return len(self) - self._operation_position

    @property
    def position(self) -> int:
        return self._operation_position

    def insert(self, operation: Operation) -> "LineMutator":
        self._mutated = True

        self._inserted_operations.append(operation)

        self._length += operation.char_n
        self._operation_position += operation.char_n

        return self

    def inject(self, operator: Operation) -> "LineMutator":
        """
        Does what insert does, but does not updates current iterator position
        """
        self._mutated = True

        self._operation_iterator.append_back(operator)
        self._length += operator.char_n

        return self

    def delete(self, char_n: int) -> OperationList:
        """
        Remove N chars from a string and return removed components list
        """
        self._mutated = True

        removed_operations = self._take(char_n)
        self._length -= char_n

        if len(removed_operations) and removed_operations[-1].line_no > 0:
            self._has_new_line = False

        return removed_operations

    def skip(self, char_n: int) -> "LineMutator":
        # drop the result
        self.take(char_n)

        return self

    def _take(self, char_n: int) -> OperationList:
        operations: OperationList = OperationList()

        while char_n:
            try:
                if not self._current_operation:
                    self._current_operation = next(self._operation_iterator)

                if self._current_operation.char_n <= char_n:
                    # take all and continue
                    operations.append(
                        deepcopy(self._current_operation)
                    )  # TODO: how to get rid of extensive deepcopy() usage?
                    char_n -= self._current_operation.char_n
                    self._current_operation = next(self._operation_iterator)
                    continue

                # take only a part
                operations.append(deepcopy(self._current_operation).rtrim(char_n, 0))
                self._current_operation.ltrim(char_n, 0)
                char_n = 0

            except StopIteration:
                break

        return operations

    def take(self, char_n: int) -> OperationList:
        operations = self._take(char_n)
        self._operation_position += char_n

        self._inserted_operations.extend(
            [deepcopy(operation) for operation in operations]
        )

        return operations

    def take_remaining(self) -> OperationList:
        return self.take(self.remaining)

    def finish(self) -> EncodedOperations:
        if not self.mutated:
            return self._operations.encode()

        self.take_remaining()

        return self._inserted_operations.encode()

    def __repr__(self) -> str:
        return f'LineMutator("{len(self._operations)}")'
