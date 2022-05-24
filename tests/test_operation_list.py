from typing import Any, Union

import pytest as pytest

from collins.operations import (
    EncodedOperations,
    Operation,
    OperationList,
    OperationTypes,
)


@pytest.mark.parametrize(
    "opcodes, expected",
    [
        (
            [OperationTypes.INSERT, OperationTypes.DELETE, OperationTypes.KEEP],
            [OperationTypes.DELETE, OperationTypes.INSERT, OperationTypes.KEEP],
        ),
        (
            [
                OperationTypes.INSERT,
                OperationTypes.KEEP,
                OperationTypes.DELETE,
                OperationTypes.INSERT,
                OperationTypes.DELETE,
                OperationTypes.INSERT,
                OperationTypes.DELETE,
            ],
            [
                OperationTypes.INSERT,
                OperationTypes.KEEP,
                OperationTypes.DELETE,
                OperationTypes.DELETE,
                OperationTypes.DELETE,
                OperationTypes.INSERT,
                OperationTypes.INSERT,
            ],
        ),
    ],
)
def test__operation_list__reorder(
    opcodes: list[OperationTypes], expected: list[OperationTypes]
) -> None:
    operations: list[Operation] = [Operation(type, 1, 0, "x") for type in opcodes]

    operation_list: OperationList = OperationList(operations)
    operation_list.reorder()

    actual_optypes: list[OperationTypes] = [
        operation.type for operation in operation_list
    ]

    assert actual_optypes == expected


@pytest.mark.parametrize(
    "raw_operations, encoded_result",
    [
        ([["+", 1, 0, "a"], ["+", 2, 0, "bc"]], "+3$abc"),
        ([["-", 1, 0, "a"], ["+", 2, 0, "bc"]], "-1+2$abc"),
        (
            [
                ["+", 1, 0, "a"],
                ["+", 2, 1, "b\n"],
                ["+", 2, 1, "c\n"],
                ["+", 2, 0, "de"],
            ],
            "|2+5+2$ab\nc\nde",
        ),
        ([["+", 1, 0, "a"], ["=", 2, 0, ""]], "+1$a"),
        ([["+", 2, 0, "ab"], ["-", 2, 0, "cd"]], "-2+2$cdab"),
        ([["+", 2, 0, "ab"], ["=", 2, 0], ["-", 2, 0, "cd"]], "+2=2-2$abcd"),
        ([["+", 2, 0, "ab"], ["=", 2, 0]], "+2$ab"),
    ],
)
def test__operation_list__encode(
    raw_operations: list[list[Union[str, int]]], encoded_result: str
) -> None:
    operation_list: OperationList = OperationList(
        operations=[Operation(*raw_operation) for raw_operation in raw_operations]
    )

    assert str(operation_list.encode()) == encoded_result


def test__operation_list__decode() -> None:
    operation_list: OperationList = OperationList.decode(
        EncodedOperations(
            encoded="|5=2p=v+1",
            char_bank="x",
        )
    )

    expected_operations: list[dict[str, Any]] = [
        {
            "type": OperationTypes.KEEP,
            "char_n": 97,
            "lines_no": 5,
        },
        {
            "type": OperationTypes.KEEP,
            "char_n": 31,
            "lines_no": 0,
        },
        {
            "type": OperationTypes.INSERT,
            "char_n": 1,
            "lines_no": 0,
        },
    ]

    for actual_operation, expected_operation in zip(
        operation_list, expected_operations
    ):
        assert actual_operation.type == expected_operation["type"]
        assert actual_operation.char_n == expected_operation["char_n"]
        assert actual_operation.line_no == expected_operation["lines_no"]
