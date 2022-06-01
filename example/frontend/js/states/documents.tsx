import { createState, State } from "@hookstate/core";

import { Document } from "../livearea/documents";

export const currentDocument: State<Document> = createState({} as Document)