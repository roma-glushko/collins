"""
 it('can insert multiline ops mid-line', function() {
    var m = new ALinesMutator(clone(sample), pool);
    var res = m.skip(2).insert(new OpComponent('+', 4, 2, null, 'X\nY\n')).finish();

    assert.deepEqual(res, [{a:'*0+1|1+3', s:'abX\n'}, {a:'|1+2', s:'Y\n'}, {a:'|1+2', s:'c\n'}, {a:'*1+4|1+1', s:'defg\n'}]);
  });
"""
import pytest as pytest
from mutators.text import TextMutator
from operations import Operation, OperationTypes


def test__text_mutator__length_calculations() -> None:
    mutator = TextMutator(["abc\n", "defg\n"])

    assert len(mutator) == 9


@pytest.mark.parametrize(
    "base_text, expected_result",
    [
        (
            ["abc\n", "defg\n"],
            ["abX\n", "Y\n", "c\n", "defg\n"],
        ),
    ],
)
def test__text_mutator__insert_multiline_ops(
    base_text: list[str], expected_result: list[str]
) -> None:
    actual_result: list[str] = (
        TextMutator(base_text)
        .skip(Operation(OperationTypes.KEEP, 2, 0))
        .insert(Operation(OperationTypes.INSERT, 4, 2, "X\nY\n"))
        .finish()
    )

    assert actual_result == expected_result


def test__test_mutator__remove_from_middle_to_the_end_and_insert():
    mutator = TextMutator(["a\n", "b\n"])

    actual_result: list[str] = (
        mutator.skip(Operation(OperationTypes.KEEP, 1, 0))
        .delete(Operation(OperationTypes.REMOVE, 3, 2))
        .insert(Operation(OperationTypes.KEEP, 1, 0, "X"))
        .finish()
    )

    assert actual_result == ["aX"]


def test__text_mutator__complex_mutations() -> None:
    mutator = TextMutator(["abcd\n", "efg\n"])

    mutator.delete(Operation(OperationTypes.REMOVE, 2, 0))
    mutator.skip(Operation(OperationTypes.KEEP, 3, 1))
    mutator.insert(Operation(OperationTypes.INSERT, 4, 2, "X\nY\n"))
    mutator.skip(Operation(OperationTypes.KEEP, 2, 0))

    mutator.delete(Operation(OperationTypes.REMOVE, 2, mutator.remaining_lines))
    mutator.insert(Operation(OperationTypes.INSERT, 1, 1, "\n"))

    assert mutator.finish() == ["cd\n", "X\n", "Y\n", "ef\n"]
