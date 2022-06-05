import * as React from "react";
import { useEffect } from "react";
import { useEmitter } from "../livearea/events/hooks";
import {Events, Message} from "../livearea/events/entities";

const BASE_URL: string = 'localhost:3003'

const DOCUMENT_ID_REGEX: RegExp = /documents\/(?<docID>[0-9]*)(\/)?$/
const documentID = (): string => DOCUMENT_ID_REGEX.exec(window.location.href).groups.docID;

export const Websocket = (): JSX.Element => {
    const eventEmitter = useEmitter()

    useEffect(() => {
        const onReceive = (event: MessageEvent) => {
            const message: Message<Events> = JSON.parse(event.data);

            eventEmitter(message.type, message.data)
        }

        const send = () => {
            // TODO: figure out what to send
            // this.socket.send(input.value)
        }

        const socket: WebSocket = new WebSocket(`ws://${BASE_URL}/documents/${documentID()}/`);
        socket.onmessage = onReceive
    })

    return <></>;
}
