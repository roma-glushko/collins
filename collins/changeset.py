import re
from typing import TYPE_CHECKING, Final, Match

from collins.encode import decode_number, encode_number
from collins.mutators.text import TextMutator
from collins.operations import (
    OPERATION_LIST_END,
    Operation,
    OperationList,
    OperationTypes,
)

if TYPE_CHECKING:
    from collins.document import Document

SIGNATURE: Final[str] = "C:"
HEADER_REGEX: Final[
    str
] = rf"{SIGNATURE}(?P<original_length>[0-9a-z]+)(?P<diff_sign>[><])(?P<new_len_diff>[0-9a-z]+)|"


class ChangeSet:
    def __init__(
        self,
        original_doc_length: int,
        operations: OperationList,
        new_doc_length: int = None,
    ) -> None:
        self.operations = operations
        self.original_doc_length = original_doc_length

        self.new_doc_length = (
            new_doc_length
            if new_doc_length is not None
            else self.original_doc_length + self.operations.delta_len()
        )

    """
    Changeset.prototype.applyTo = function(doc) {
      var mut = doc.mutate();
      this._ops.reorder();
      this._ops.map(function(op, index) {
        // if we reuse (don't pack) changeset object, we can end up with
        // empty operations sometimes, do not process them.
        if(op.chars == 0) {
          return;
        }
    
        if(op.opcode == OpComponent.INSERT) {
          mut.insert(op);
        } else if (op.opcode == OpComponent.REMOVE) {
          // Since we can have multiline remove ops, remove() can
          // return an array of components instead of single one.
          // But since they all should be mergeable, we can run a quick
          // reduce operation and compare the result
          var removed = mut.remove(op.chars, op.lines)
                          .reduce(function(prev, op) {
                            return prev.append(op);
                          }, new OpComponent());
    
          assert(removed.equals(op, true), 'actual does not match removed');
        } else if (op.opcode == OpComponent.KEEP) {
          if(op.attribs.isEmpty()) {
            mut.skip(op.chars, op.lines);
          } else {
            mut.applyFormat(op);
          }
        }
      });
      mut.finish();
    
      assert.equal(this._newLen, doc.length(), 'final document length does not match');
      return doc;
    };
    """

    def __call__(self, document: "Document") -> "Document":
        """
        Apply changeset to the document, modifying it in-place.
        """
        text_mutator: TextMutator = document.mutate()
        self.operations.reorder()

        for operation in self.operations:
            # if we reuse (don't pack) changeset object, we can end up with
            # empty operations sometimes, do not process them.
            if not operation.char_n:
                continue

            if operation.type == OperationTypes.INSERT:
                text_mutator.insert(operation)

            if operation.type == OperationTypes.REMOVE:
                """
                Since we can have multiline remove ops, remove() can
                return an array of components instead of single one.
                But since they all should be mergeable, we can run a quick
                reduce operation and compare the result
                """
                text_mutator.delete(operation)

            if operation.type == OperationTypes.KEEP:
                text_mutator.skip(operation)

        text_mutator.finish()

        return document

    def compose(self, changeset: "ChangeSet") -> "ChangeSet":
        """
        Compose this changeset with other changeset, producing cumulative result of both changes
        """

        self.operations.reorder()
        changeset.operations.reorder()

        """
        var newOps = util.zip(this._ops, otherCS._ops, 
    function(thisOp, otherOp) {
      var noSplit = thisOp.opcode == OpComponent.REMOVE || otherOp.opcode == OpComponent.INSERT;
      // KEEPS can be replaced by REMOVEs
      var hasKeep = thisOp.opcode == OpComponent.KEEP || otherOp.opcode == OpComponent.KEEP;
      // REMOVEs can affect KEEPs and INSERTs but not other REMOVEs
      var hasRemoveActual = (thisOp.opcode != otherOp.opcode) && (thisOp.opcode == OpComponent.REMOVE || otherOp.opcode == OpComponent.REMOVE); 
      // in both cases we can split ops into equal slices
      return (hasKeep || hasRemoveActual) && !noSplit;
    },
    function(thisOp, otherOp, opOut) {
      if (thisOp.opcode == OpComponent.REMOVE || !otherOp.opcode) {
        // if we've removed something, it cannot be undone by next op
        thisOp.copyTo(opOut);
        thisOp.skip();
      } else if (otherOp.opcode == OpComponent.INSERT || !thisOp.opcode) {
        // if other is inserting something it should be inserted
        otherOp.copyTo(opOut);
        otherOp.skip();
      } else {
        if(otherOp.opcode == OpComponent.REMOVE) {
          // at this point we're operating on actual chars (KEEP or INSERT) in the target string
          // we don't validate KEEPs since they just add format and not keep final attributes list
          var validRemove = (thisOp.opcode == OpComponent.KEEP) || thisOp.equals(otherOp, true);
          assert(validRemove, 'removed in composition does not match original' + JSON.stringify(thisOp) + JSON.stringify(otherOp));

          // if there was no insert on our side, just keep the other op,
          // overwise we're removing what was inserted and will skip both
          if (thisOp.opcode == OpComponent.KEEP) {
            // undo format changes made by thisOp and compose with otherOp
            otherOp.copyTo(opOut)
              .composeAttributes(thisOp.attribs.invert());
          }
        } else if(otherOp.opcode == OpComponent.KEEP) {
          // here, thisOp is also KEEP or INSERT, so just copy it over and compose with
          // otherOp
          thisOp.copyTo(opOut)
            .composeAttributes(otherOp.attribs);
        }

        thisOp.skip();
        otherOp.skip();
      }
    });
        """

        def split(first_op: Operation, second_op: Operation) -> bool:
            no_split: bool = (
                first_op.type == OperationTypes.REMOVE
                or second_op.type == OperationTypes.INSERT
            )

            # KEEPS can be replaced by REMOVEs
            has_keep: bool = (
                first_op.type == OperationTypes.KEEP
                or second_op.type == OperationTypes.KEEP
            )

            # REMOVEs can affect KEEPs and INSERTs but not other REMOVEs
            has_remove_actual: bool = (first_op.type != second_op.type) and (
                first_op.type == OperationTypes.REMOVE
                or second_op.type == OperationTypes.REMOVE
            )

            return (has_keep or has_remove_actual) and not no_split

        composed_operations = []

        return ChangeSet(
            original_doc_length=self.original_doc_length,
            new_doc_length=changeset.new_doc_length,
            operations=composed_operations,
        )

    def invert(self) -> "ChangeSet":
        inverted_operations = self.operations.invert()

        return ChangeSet(
            original_doc_length=self.original_doc_length,
            new_doc_length=self.new_doc_length,
            operations=inverted_operations,
        )

    def transform(self, first_op: Operation, second_op: Operation) -> "ChangeSet":
        """
        Transform this changeset against other changeset.

        explanation for side = [left | right]
        let's say we have thisOp coming to server after otherOp,
        both creating a "tie" situation.
        server has [otherOp, thisOp]
        for server otherOp is already written, so it transforms thisOp
        by otherOp, taking otherOp as first-win and thisOp as second.
        In [otherOp, thisOp] list otherOp is on the "left"

        Server sends its otherOp back to the client, but client already
        applied thisOp operation, so his queue looks like
        [thisOp, otherOp]
        Client should transorm otherOp, and to get same results as server,
        this time it should take otherOp as first-win. In the list
        otherOp is to the "right"
        """
        pass

    def encode(self) -> str:
        enc_operations = self.operations.encode()

        encoded_original_length: str = encode_number(self.original_doc_length)
        encoded_len_diff: str = f"{'>' if enc_operations.delta_len >= 0 else '<'}{encode_number(abs(enc_operations.delta_len))}"

        return (
            f"{SIGNATURE}"
            f"{encoded_original_length}{encoded_len_diff}{str(enc_operations)}"
        )

    @classmethod
    def decode(cls, serialized_changeset: str) -> "ChangeSet":
        header_part_matches: Match[str] = re.search(HEADER_REGEX, serialized_changeset)

        if not header_part_matches:
            pass

        original_doc_length: int = decode_number(
            header_part_matches.group("original_length")
        )
        len_diff_sign: int = 1 if header_part_matches.group("diff_sign") == ">" else -1
        len_delta: int = decode_number(header_part_matches.group("new_len_diff"))

        new_doc_length: int = original_doc_length + len_diff_sign * len_delta

        header_length: int = len(header_part_matches[0])
        operation_list_end: int = serialized_changeset.find(OPERATION_LIST_END)

        serialized_operations: str = serialized_changeset[
            header_length:operation_list_end
        ]
        char_bank: str = serialized_changeset[operation_list_end + 1 :]

        return cls(
            original_doc_length=original_doc_length,
            new_doc_length=new_doc_length,
            operations=OperationList.decode(serialized_operations, char_bank),
        )
