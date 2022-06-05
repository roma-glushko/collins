import * as React from "react";
import {MutableRefObject, useEffect, useRef} from "react";
import {useEmitter, useEvent} from "../livearea/events/hooks";
import {Events, EventTypes, Message} from "../livearea/events/entities";

const BASE_URL: string = 'localhost:3003'

const DOCUMENT_ID_REGEX: RegExp = /documents\/(?<docID>[0-9]*)(\/)?.*$/
const parseDocumentID = (): string => DOCUMENT_ID_REGEX.exec(window.location.href).groups.docID;

export const Websocket = (): JSX.Element => {
    const websocket: MutableRefObject<WebSocket | null> = useRef<WebSocket|null>(null)
    const eventEmitter = useEmitter()

    function sendMessage<T extends Events>(eventType: keyof T, data: T[keyof T]): void {
        const message: Message<T> = {
            type: eventType,
            data: data,
        }

        websocket.current.send(JSON.stringify(message))
    }

    useEffect(() => {
        const documentID: string = parseDocumentID()
        const socket = new WebSocket(`ws://${BASE_URL}/documents/${documentID}/`)

        socket.onmessage = (event: MessageEvent) => {
            const message: Message<Events> = JSON.parse(event.data);

            eventEmitter(message.type, message.data)
        }

        websocket.current = socket
    }, [])

    useEvent(EventTypes.commit_changes, (data): void => {
        if (!websocket.current) {
            console.warn(
                `Websocket connection has not been established yet.` +
                `Could not send '${EventTypes.commit_changes}' event`
            )
            return
        }

        console.log(data)
        sendMessage<Events>(EventTypes.commit_changes, data)
    })

    return <></>;
}
