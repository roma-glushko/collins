from typing import Any

from collins.changeset import ChangeSet, Operation, OperationTypes


def test__changeset__decode() -> None:
    changeset: ChangeSet = ChangeSet.decode("Z:5g>1|5=2p=v*4*5+1$x")

    assert changeset.char_bank == "x"

    assert changeset.original_doc_length == 196
    assert changeset.new_doc_length == 197

    assert changeset.operations == "|5=2p=v*4*5+1"


def test__changeset__encode() -> None:
    changeset: ChangeSet = ChangeSet(
        original_doc_length=196,
        new_doc_length=197,
        operations="|5=2p=v*4*5+1",
        char_bank="x",
    )

    assert changeset.encode() == "Z:5g>1|5=2p=v*4*5+1$x"


def test__operation__decode() -> None:
    operations: list[Operation] = list(Operation.decode("|5=2p=v*4*5+1"))

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

    for actual_operation, expected_operation in zip(operations, expected_operations):
        assert actual_operation.dict() == expected_operation
