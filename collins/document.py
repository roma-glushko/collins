from collins.mutators.text import TextMutator


class Document:
    def __init__(self, text: list[str] = None) -> None:
        self._text: list[str] = text or []

    def mutate(self) -> TextMutator:
        return TextMutator(text=self._text)

    @classmethod
    def from_text(cls, text: str) -> "Document":
        pass

    def __len__(self) -> int:
        pass

    @classmethod
    def decode(cls) -> "Document":
        pass

    def encode(self) -> None:
        pass