import pytest
from mutators.line import LineMutator
from operations import EncodedOperations


@pytest.fixture
def empty_operations() -> EncodedOperations:
    return EncodedOperations()


def test__line_mutator__empty_string(empty_operations) -> None:
    mutator = LineMutator(empty_operations)

    assert str(mutator.take_remaining().encode()) == "$"
    assert not mutator.mutated


"""
it('supports newline at the end', function() {
    var m = new AStringMutator({ a: '*0+4|1+1', s: 'abcd\n' }, pool);
    assert.deepEqual(m.takeRemaining(), clist([['+',4,0,'*0','abcd'],['+',1,1,null,'\n']]));
  });
"""


def test__line_mutator__newline_at_the_end() -> None:
    mutator = LineMutator(EncodedOperations(encoded="+4|1+1", char_bank="abcd\n"))

    assert str(mutator.take_remaining().encode()) == ""


def test__line_mutator__decompose_into_subcomponents() -> None:
    mutator = LineMutator(EncodedOperations(encoded="+12", char_bank="abcdefghijkl"))

    operations = mutator.skip(1).take(2)
    assert str(operations.encode()) == "+2$bc"

    operations = mutator.take(1)
    assert str(operations.encode()) == "+1$d"

    operations = mutator.take_remaining()
    assert str(operations.encode()) == "+8$efghijkl"
