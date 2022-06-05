import re
from typing import Optional

from collins.changeset import Changeset
from collins.document import Document
from collins.operations import OperationList

NEW_LINE_PATTERN: str = r"\n"


class ChangesetBuilder:
    def __init__(self, document: Optional["Document"] = None) -> None:
        self._document = document or Document()
        self._text_mutator = self._document.mutate()
        self._original_doc_len = len(self._document)

        self._operations = OperationList()

    def insert(self, text: str) -> "ChangesetBuilder":
        """ """
        last_new_line: int = text.rfind("\n")

        if last_new_line < 0:
            # single line lines
            self._operations.append_insert(len(text), 0, text)
            pass

        if last_new_line >= 0:
            # multiline lines, insert everything before last newline as multiline op
            last_char_idx: int = last_new_line + 1
            lines_num: int = len(
                re.match(NEW_LINE_PATTERN, text, re.MULTILINE).groups()
            )
            self._operations.append_insert(
                last_char_idx, lines_num, text[:last_char_idx]
            )

            if last_new_line < len(text):
                # insert remainder as single-line op
                self._operations.append_insert(
                    len(text) - last_char_idx, 0, text[last_char_idx:]
                )

        return self

    def delete(self, char_n: int, line_no: int) -> "ChangesetBuilder":
        """
        Builder.prototype.remove = function(N, L) {
          this._ops.concat(this._mut.take(N, L).invert());
          return this;
        };
        """
        self._operations.extend(
            self._text_mutator.take(char_n, line_no).invert().operations
        )

        return self

    def finish(self) -> "Changeset":
        return Changeset(self._original_doc_len, self._operations)

    @classmethod
    def from_text(cls, text: str) -> "Changeset":
        builder: "ChangesetBuilder" = cls()
        builder.insert(text)

        return builder.finish()
