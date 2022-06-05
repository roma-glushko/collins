import * as React from "react";
import {useEmitter, useEvent} from "../livearea/events/hooks";
import {CommitChangesData, EventTypes} from "../livearea/events/entities";
import { currentDocument } from "../states/documents";
import { useState } from "@hookstate/core";

import "./Textarea.css"
import textarea from "./Textarea";

type TextareaProps = {
    children?: JSX.Element | JSX.Element[]
}

const Textarea = (props: TextareaProps): JSX.Element => {
    const isSyncing = useState(false)
    const document = useState(currentDocument)
    const docText = useState(currentDocument.text)
    const emit = useEmitter()

    useEvent(EventTypes.document_opened, (data) => {
        document.set(data.document);
        docText.set(data.document.text);
    })

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        docText.set(event.target.value)
    }

    const handleInput = (event: React.FormEvent<HTMLTextAreaElement>): void => {
        const textarea: HTMLTextAreaElement = event.target as HTMLTextAreaElement
        const inputEvent: InputEvent = event.nativeEvent as InputEvent

        console.log(`[Input] Text was ${inputEvent.inputType} "${inputEvent.data}" 
        at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    const handleSelect = (event: React.SyntheticEvent<HTMLTextAreaElement>): void => {
        const textarea: HTMLTextAreaElement = event.target as HTMLTextAreaElement

        console.log(`Selection at ${textarea.selectionStart}:${textarea.selectionEnd}`)
    }

    const submitSampleChangeset = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault()

        emit(EventTypes.commit_changes, {
            base_revision: document.get().revision_id,
            changeset: "C:hm>4+4$test",
        } as CommitChangesData)
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
        <button onClick={(event) => submitSampleChangeset(event)}>Submit Sample Changeset</button>
        <p className={`revision`}>rev: {document.get().revision_id}</p>
    </form>
}

export default Textarea