import pytest

from collins.mutators.text import TextMutator
from collins.operations import EncodedOperations, Operation


def test__text_mutator__length_calculations() -> None:
    mutator = TextMutator(
        [
            EncodedOperations(encoded="+1|1+3", char_bank="abc\n"),
            EncodedOperations(encoded="+4|1+1", char_bank="defg\n"),
        ]
    )

    assert len(mutator) == 9


@pytest.mark.parametrize(
    "base_text, expected_result",
    [
        (
            [
                EncodedOperations(encoded="+1|1+3", char_bank="abc\n"),
                EncodedOperations(encoded="+4|1+1", char_bank="defg\n"),
            ],
            [
                EncodedOperations(encoded="+1|1+3", char_bank="abX\n"),
                EncodedOperations(encoded="|1+2", char_bank="Y\n"),
                EncodedOperations(encoded="|1+2", char_bank="c\n"),
                EncodedOperations(encoded="+4|1+1", char_bank="defg\n"),
            ],
        ),
    ],
)
def test__text_mutator__insert_multiline_ops(
    base_text: list[EncodedOperations], expected_result: list[str]
) -> None:
    actual_result: list[EncodedOperations] = (
        TextMutator(base_text)
        .skip(Operation.keep(2, 0))
        .insert(Operation.insert(4, 2, "X\nY\n"))
        .finish()
    )

    assert actual_result == expected_result


def test__test_mutator__remove_from_middle_to_the_end_and_insert() -> None:
    mutator = TextMutator(
        [
            EncodedOperations(encoded="|1+2", char_bank="a\n"),
            EncodedOperations(encoded="|1+2", char_bank="b\n"),
        ]
    )

    results: list[EncodedOperations] = (
        mutator.skip(Operation.keep(1, 0))
        .delete(Operation.delete(3, 2))
        .insert(Operation.insert(1, 0, "X"))
        .finish()
    )

    assert len(results) == 1, results

    actual_result = results[0]

    assert str(actual_result) == ["|1+2$aX"]


def test__text_mutator__complex_mutations() -> None:
    mutator = TextMutator(
        [
            EncodedOperations(encoded="|1+5", char_bank="abcd\n"),
            EncodedOperations(encoded="|1+4", char_bank="efg\n"),
        ]
    )

    mutator.delete(Operation.delete(2, 0))
    mutator.skip(Operation.keep(3, 1))
    mutator.insert(Operation.insert(4, 2, "X\nY\n"))
    mutator.skip(Operation.keep(2, 0))

    mutator.delete(Operation.delete(2, mutator.remaining_lines))
    mutator.insert(Operation.insert(1, 1, "\n"))

    assert mutator.finish() == ["cd\n", "X\n", "Y\n", "ef\n"]
