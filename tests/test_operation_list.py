import pytest as pytest

from collins.operations import Operation, OperationList, OperationTypes


@pytest.mark.parametrize(
    "opcodes, expected",
    [
        (
            [OperationTypes.INSERT, OperationTypes.REMOVE, OperationTypes.KEEP],
            [OperationTypes.REMOVE, OperationTypes.INSERT, OperationTypes.KEEP],
        ),
        (
            [
                OperationTypes.INSERT,
                OperationTypes.KEEP,
                OperationTypes.REMOVE,
                OperationTypes.INSERT,
                OperationTypes.REMOVE,
                OperationTypes.INSERT,
                OperationTypes.REMOVE,
            ],
            [
                OperationTypes.INSERT,
                OperationTypes.KEEP,
                OperationTypes.REMOVE,
                OperationTypes.REMOVE,
                OperationTypes.REMOVE,
                OperationTypes.INSERT,
                OperationTypes.INSERT,
            ],
        ),
    ],
)
def test__operations__reorder(
    opcodes: list[OperationTypes], expected: list[OperationTypes]
) -> None:
    operations: list[Operation] = [Operation(type, 1, 0, "", "x") for type in opcodes]

    operation_list: OperationList = OperationList(operations)
    operation_list.reorder()

    actual_optypes: list[OperationTypes] = [
        operation.type for operation in operation_list.operations
    ]

    assert actual_optypes == expected
