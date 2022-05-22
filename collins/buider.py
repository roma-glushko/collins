from collins.changeset import ChangeSet
from collins.operations import OperationList


class ChangeSetBuilder:
    def __init__(self, document) -> None:
        self.document = document

        self.operations = OperationList()

    def insert(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def finish(self) -> "ChangeSet":
        return ChangeSet()