from collins.operations import Operation


def test__operation__skip() -> None:
    expected_operation: Operation = Operation(type=None)
