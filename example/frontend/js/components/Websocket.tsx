import * as React from "react";
import {useEffect} from "react";
import {createState, State, useState} from "@hookstate/core";

export const receivedMessages: State<string[]> = createState([]) as State<string[]>;

const BASE_URL: string = 'localhost:3003'

export const Websocket = (props: {sessionID: string}) => {
    const messages = useState(receivedMessages);

    useEffect(() => {
        const onReceive = (event: MessageEvent) => {
            messages.merge([event.data])
        }

        const send = () => {
        // TODO: figure out what to send
        // this.socket.send(input.value)
        }

        const socket = new WebSocket(`ws://${BASE_URL}/ws/${props.sessionID}`);
        socket.onmessage = onReceive
    })

    return <></>;
}
