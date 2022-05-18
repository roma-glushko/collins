from typing import Any

import pytest as pytest

from collins.changeset import ChangeSet
from collins.operations import OperationList, OperationTypes


def test__changeset__decode() -> None:
    changeset: ChangeSet = ChangeSet.decode("C:5g>1|5=2p=v*4*5+1$x")

    assert changeset.char_bank == "x"

    assert changeset.original_doc_length == 196
    assert changeset.new_doc_length == 197

    assert changeset.operations == "|5=2p=v*4*5+1"


def test__changeset__encode() -> None:
    changeset: ChangeSet = ChangeSet(
        original_doc_length=196,
        new_doc_length=197,
        operations="|5=2p=v*4*5+1",
        # char_bank="x",
    )

    assert changeset.encode() == "Z:5g>1|5=2p=v*4*5+1$x"


def test__operation__decode() -> None:
    operation_list: OperationList = OperationList.decode("|5=2p=v*4*5+1", "x")

    expected_operations: list[dict[str, Any]] = [
        {
            "type": OperationTypes.KEEP,
            "char_num": 97,
            "lines": 5,
            "attributes": "",
        },
        {
            "type": OperationTypes.KEEP,
            "char_num": 31,
            "lines": 0,
            "attributes": "",
        },
        {
            "type": OperationTypes.INSERT,
            "char_num": 1,
            "lines": 0,
            "attributes": "*4*5",
        },
    ]

    for actual_operation, expected_operation in zip(
        operation_list.operations, expected_operations
    ):
        assert actual_operation == expected_operation


@pytest.mark.parametrize(
    "enc_changeset_one, enc_changeset_two, result_changeset",
    [
        ("C:0>3+3$abc", "C:3>3=3+3$def", "C:0>6+6$abcdef"),
        ("C:0>2+2$ab", "C:2>1|1+1$\n", "C:0>3|1+1+2$\nab"),
        ("X:0>3+3$abc", "X:3<1=1-1$b", "X:0>2+2$ac"),
    ],
)
def test__changeset__compose(
    enc_changeset_one: str, enc_changeset_two: str, result_changeset: str
) -> None:
    changeset_one: ChangeSet = ChangeSet.decode(enc_changeset_one)
    changeset_two: ChangeSet = ChangeSet.decode(enc_changeset_two)

    composed_changeset: ChangeSet = changeset_one.compose(changeset_two)

    assert result_changeset == composed_changeset.encode()
