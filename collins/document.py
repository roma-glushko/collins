from typing import TYPE_CHECKING

from collins.mutators.text import TextMutator
from collins.operations import EncodedOperations

if TYPE_CHECKING:
    from collins.changeset import Changeset


class Document:
    def __init__(self, lines: list[EncodedOperations] = None) -> None:
        self._lines: list[EncodedOperations] = lines or []

    def mutate(self) -> TextMutator:
        return TextMutator(lines=self._lines)

    @classmethod
    def from_text(cls, text: str) -> "Document":
        from collins.builder import ChangesetBuilder

        builder: ChangesetBuilder = ChangesetBuilder()
        builder.insert(text)

        changeset: "Changeset" = builder.finish()

        return changeset(Document())

    def __len__(self) -> int:
        return sum([len(line.char_bank) for line in self._lines])

    @classmethod
    def decode(cls) -> "Document":
        pass

    def encode(self) -> None:
        pass
