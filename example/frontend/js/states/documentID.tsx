import {createState, State} from "@hookstate/core";

const DOCUMENT_ID_REGEX: RegExp = /documents\/(?<docID>[0-9]*)(\/)?$/

export const documentID: State<string> = createState(() => DOCUMENT_ID_REGEX.exec(window.location.href).groups.docID);
