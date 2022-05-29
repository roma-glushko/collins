import pytest as pytest

from collins.changeset import Changeset, TransformSides
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
        ("C:0>3+3$abc", "C:3<1=1-1$b", "C:0>2+2$ac"),
        ("C:0>3+3$abc", "C:3<1-2+1$abd", "C:0>2+2$dc"),
        # test ParallelOperationIterator
        ("C:8<4-4$abcd", "C:4<2|2-2$\n\n", "C:8<6|2-6$abcd\n\n"),
        ("C:4>0=2", "C:4<2-2$ab", "C:4<2-2$ab"),
        ("C:3<3|1-3$12\n", "C:0>2+2$XY", "C:3<1|1-3+2$12\nXY"),
    ],
)
def test__changeset__compose(
    enc_changeset_one: str, enc_changeset_two: str, result_changeset: str
) -> None:
    changeset_one: Changeset = Changeset.decode(enc_changeset_one)
    changeset_two: Changeset = Changeset.decode(enc_changeset_two)

    composed_changeset: Changeset = changeset_one.compose(changeset_two)

    assert composed_changeset.encode() == result_changeset


@pytest.mark.parametrize(
    "enc_changeset_one, enc_changeset_two, side, result_changeset",
    [
        ("C:0>2+2$ab", "C:0>2+2$cd", TransformSides.LEFT, "C:2>2=2+2$ab"),
        ("C:0>2+2$cd", "C:0>2+2$ab", TransformSides.RIGHT, "C:2>2+2$cd"),
        ("C:0>2+2$ab", "C:0>1|1+1$\n", TransformSides.LEFT, "C:1>2+2$ab"),
        ("C:0>2+2$ab", "C:0>1|1+1$\n", TransformSides.RIGHT, "C:1>2+2$ab"),
        (
            "C:0>2|1+1+1$\na",
            "C:0>2|1+1+1$\nb",
            TransformSides.LEFT,
            "C:2>2|1=1=1|1+1+1$\na",
        ),
        ("C:0>2|1+1+1$\nb", "C:0>2|1+1+1$\na", TransformSides.RIGHT, "C:2>2|1+1+1$\nb"),
        ("C:2>1+1$a", "C:2<1-1$b", TransformSides.LEFT, "C:1>1+1$a"),
        ("C:2>1+1$a", "C:2<1-1$b", TransformSides.RIGHT, "C:1>1+1$a"),
        ("C:8<4-4$abcd", "C:8<2-2$ab", TransformSides.LEFT, "C:6<2-2$cd"),
        ("C:8<2-2$ab", "C:8<4-4$abcd", TransformSides.LEFT, "C:4>0$"),
        ("C:8<2-2$ab", "C:8>0=4", TransformSides.LEFT, "C:8<2-2$ab"),
        ("C:8>2=8+2$ab", "C:8<4-4$abcd", TransformSides.LEFT, "C:4>2=4+2$ab"),
        ("C:8>2=4+2$ab", "C:8<6-6$abcdef", TransformSides.LEFT, "C:2>2+2$ab"),
        ("C:4>1|1=4+1$a", "C:4>5+5$bcdef", TransformSides.LEFT, "C:9>1|1=9+1$a"),
    ],
)
def test__changeset__transform(
    enc_changeset_one: str,
    enc_changeset_two: str,
    side: TransformSides,
    result_changeset: str,
) -> None:
    changeset_one: Changeset = Changeset.decode(enc_changeset_one)
    changeset_two: Changeset = Changeset.decode(enc_changeset_two)

    transformed_changeset: Changeset = changeset_one.transform(changeset_two, side)

    assert transformed_changeset.encode() == result_changeset
