from typing import TYPE_CHECKING

from collins.builder import ChangesetBuilder
from collins.mutators.text import TextMutator

if TYPE_CHECKING:
    from collins.changeset import Changeset


class Document:
    def __init__(self, lines: list[str] = None) -> None:
        self._lines: list[str] = lines or []

    def mutate(self) -> TextMutator:
        return TextMutator(lines=self._lines)

    @classmethod
    def from_text(cls, text: str) -> "Document":
        builder: ChangesetBuilder = ChangesetBuilder()
        builder.insert(text)

        changeset: "Changeset" = builder.finish()

        return changeset(Document())

    def __len__(self) -> int:
        pass

    @classmethod
    def decode(cls) -> "Document":
        pass

    def encode(self) -> None:
        pass
