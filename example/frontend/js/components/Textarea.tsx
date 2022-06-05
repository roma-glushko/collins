import * as React from "react";
import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import { currentDocument } from "../states/documents";
import { useState } from "@hookstate/core";

import "./Textarea.css"
import textarea from "./Textarea";

type TextareaProps = {
    children?: JSX.Element | JSX.Element[]
}

const Textarea = (props: TextareaProps): JSX.Element => {
    const isSyncing = useState(true)
    const document = useState(currentDocument)
    const docText = useState(currentDocument.text)

    useEvent(EventTypes.document_opened, (data) => {
        document.set(data.document);
        docText.set(data.document.text);
    })

    const handleInput = (event: React.FormEvent<HTMLTextAreaElement>) => {
        const textarea: HTMLTextAreaElement = event.target
        const inputEvent: InputEvent = event.nativeEvent

        console.log(event)
        console.log(`[Input] Text was ${inputEvent.inputType} "${inputEvent.data}" 
        at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    function handleSelect(event: React.SyntheticEvent<HTMLTextAreaElement>) {
        const textarea: HTMLTextAreaElement = event.target

        console.log(event)
        console.log(`Selection at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    return <form action="">
        <h2>{ document.get().title }</h2>
        { props.children }
        { isSyncing.get() && <p className={`syncing-status`}>syncing 🔄</p> }
        <textarea
            className={`editbox`}
            value={docText.get()}
            rows={30}
            cols={50}
            autoComplete="off"
            onChange={(event) => docText.set(event.target.value)}
            onInput={event => handleInput(event)}
            onSelect={event => handleSelect(event)}
        >
        </textarea>
        <p className={`revision`}>rev: {document.get().revision_id}</p>
    </form>
}

export default Textarea