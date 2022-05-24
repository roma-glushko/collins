from buider import ChangeSetBuilder
from changeset import ChangeSet

from collins.mutators.text import TextMutator


class Document:
    def __init__(self, lines: list[str] = None) -> None:
        self._lines: list[str] = lines or []

    def mutate(self) -> TextMutator:
        return TextMutator(lines=self._lines)

    @classmethod
    def from_text(cls, text: str) -> "Document":
        builder: ChangeSetBuilder = ChangeSetBuilder()
        builder.insert(text)

        changeset: ChangeSet = builder.finish()

        return changeset(Document())

    def __len__(self) -> int:
        pass

    @classmethod
    def decode(cls) -> "Document":
        pass

    def encode(self) -> None:
        pass