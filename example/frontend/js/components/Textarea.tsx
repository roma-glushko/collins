import * as React from "react";
import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import { currentDocument } from "../states/documents";
import { useState } from "@hookstate/core";

import "./Textarea.css"
import textarea from "./Textarea";
import {ChangeEventHandler} from "react";

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

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        docText.set(event.target.value)
    }

    const handleInput = (event: React.FormEvent<HTMLTextAreaElement>): void => {
        const textarea: HTMLTextAreaElement = event.target
        const inputEvent: InputEvent = event.nativeEvent

        console.log(`[Input] Text was ${inputEvent.inputType} "${inputEvent.data}" 
        at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    const handleSelect = (event: React.SyntheticEvent<HTMLTextAreaElement>): void => {
        const textarea: HTMLTextAreaElement = event.target

        console.log(`Selection at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    return <form action="">
        <h2>{ document.get().title }</h2>
        { props.children }
        { isSyncing.get() && <p className={`syncing-status`}>🔄 syncing..</p> }
        <textarea
            className={`editbox`}
            rows={25}
            cols={50}
            autoComplete="off"
            onChange={event => handleChange(event)}
            onInput={event => handleInput(event)}
            onSelect={event => handleSelect(event)}
            value={docText.get()}
        >
        </textarea>
        <p className={`revision`}>rev: {document.get().revision_id}</p>
    </form>
}

export default Textarea