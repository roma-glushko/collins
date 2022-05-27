import pytest as pytest

from collins.changeset import Changeset
from collins.operations import EncodedOperations, OperationList


def test__changeset__decode() -> None:
    changeset: Changeset = Changeset.decode("C:5g>1|5=2p=v+1$x")

    assert changeset.original_doc_length == 196
    assert changeset.new_doc_length == 197

    encoded_operations = changeset.operations.encode()

    assert str(encoded_operations) == "|5=2p=v+1$x"
    assert encoded_operations.char_bank == "x"


def test__changeset__encode() -> None:
    changeset: Changeset = Changeset(
        original_doc_length=196,
        new_doc_length=197,
        operations=OperationList.decode(
            EncodedOperations(
                encoded="|5=2p=v+1",
                char_bank="x",
            )
        ),
    )

    assert changeset.encode() == "C:5g>1|5=2p=v+1$x"


@pytest.mark.parametrize(
    "enc_changeset_one, enc_changeset_two, result_changeset",
    [
        ("C:0>3+3$abc", "C:3>3=3+3$def", "C:0>6+6$abcdef"),
        ("C:0>2+2$ab", "C:2>1|1+1$\n", "C:0>3|1+1+2$\nab"),
        # ("C:0>3+3$abc", "C:3<1=1-1$b", "C:0>2+2$ac"),
    ],
)
def test__changeset__compose(
    enc_changeset_one: str, enc_changeset_two: str, result_changeset: str
) -> None:
    changeset_one: Changeset = Changeset.decode(enc_changeset_one)
    changeset_two: Changeset = Changeset.decode(enc_changeset_two)

    composed_changeset: Changeset = changeset_one.compose(changeset_two)

    assert result_changeset == composed_changeset.encode()
