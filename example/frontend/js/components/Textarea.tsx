import * as React from "react";
import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import { currentDocument } from "../states/documents";
import { useState } from "@hookstate/core";

type TextareaProps = {
    children?: JSX.Element | JSX.Element[]
}

const Textarea = (props: TextareaProps): JSX.Element => {
    const document = useState(currentDocument)

    useEvent(EventTypes.document_opened, (data) => {
        document.set(data.document)
    })

    return <form action="">
        <h2>{ document.get().title }</h2>
        { props.children }
        <textarea
            value={document.get().body}
            rows={30}
            cols={50}
            autoComplete="off">
        </textarea>
    </form>
}

export default Textarea