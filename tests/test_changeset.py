from collins.changeset import ChangeSet


def test__changeset__decode() -> None:
    changeset: ChangeSet = ChangeSet.decode("Z:5g>1|5=2p=v*4*5+1$x")

    assert changeset.char_bank == "x"

    assert changeset.original_doc_length == 196
    assert changeset.new_doc_length == 197

    assert changeset.operations == "|5=2p=v*4*5+1"

def test__changeset__encode() -> None:
    changeset: ChangeSet = ChangeSet(
        original_doc_length=196,
        new_doc_length=197,
        operations="|5=2p=v*4*5+1",
        char_bank="x"
    )

    assert changeset.encode() == "Z:5g>1|5=2p=v*4*5+1$x"
