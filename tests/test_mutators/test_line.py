import pytest

from collins.mutators.line import LineMutator
from collins.operations import EncodedOperations, Operation, OperationList


@pytest.fixture
def empty_operations() -> EncodedOperations:
    return EncodedOperations()


def test__line_mutator__empty_string(empty_operations) -> None:
    mutator = LineMutator(empty_operations)

    assert str(mutator.take_remaining().encode()) == "$"
    assert not mutator.mutated


def test__line_mutator__newline_at_the_end() -> None:
    mutator = LineMutator(EncodedOperations(encoded="+4|1+1", char_bank="abcd\n"))

    assert mutator.take_remaining() == OperationList(
        [
            Operation.insert(4, 0, "abcd"),
            Operation.insert(1, 1, "\n"),
        ]
    )


def test__line_mutator__decompose_into_subcomponents() -> None:
    mutator = LineMutator(EncodedOperations(encoded="+12", char_bank="abcdefghijkl"))

    operations = mutator.skip(1).take(2)
    assert str(operations.encode()) == "+2$bc"

    operations = mutator.take(1)
    assert str(operations.encode()) == "+1$d"

    operations = mutator.take_remaining()
    assert str(operations.encode()) == "+8$efghijkl"
