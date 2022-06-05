import * as React from "react";
import {useEffect, useRef} from "react";
import {useEmitter, useEvent} from "../livearea/events/hooks";
import {Events, EventTypes, Message} from "../livearea/events/entities";

const BASE_URL: string = 'localhost:3003'

const DOCUMENT_ID_REGEX: RegExp = /documents\/(?<docID>[0-9]*)(\/)?.*$/
const parseDocumentID = (): string => DOCUMENT_ID_REGEX.exec(window.location.href).groups.docID;

export const Websocket = (): JSX.Element => {
    const websocket = useRef<WebSocket|null>(null)
    const eventEmitter = useEmitter()

    useEffect(() => {
        const documentID: string = parseDocumentID()
        const socket = new WebSocket(`ws://${BASE_URL}/documents/${documentID}/`)

        socket.onmessage = (event: MessageEvent) => {
            const message: Message<Events> = JSON.parse(event.data);

            eventEmitter(message.type, message.data)
        }

        websocket.current = socket
    }, [])

    useEvent(EventTypes.commit_changes, (data) => {
        if (!websocket.current) {
            console.warn(
                `Websocket connection has not been established yet.` +
                `Could not send '${EventTypes.commit_changes}' event`
            )
            return
        }

        const message: Message<Events> = {
            type: EventTypes.commit_changes,
            data: {
                base_revision: data.base_revision,
                changeset: data.changeset,
            }
        }

        console.log(message)
        websocket.current.send(JSON.stringify(message))
    })

    return <></>;
}
