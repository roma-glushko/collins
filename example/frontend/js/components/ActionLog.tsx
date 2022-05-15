import * as React from 'react';
import { receivedMessages } from "./Websocket";
import { useState } from "@hookstate/core";

const ActionLog = () => {
    const messages = useState(receivedMessages);

    return <>
        <h3>Action Log</h3>
        <ul id="actions">
        {messages.get().map((message: string, messageIndex: number) =>
            <li key={messageIndex}>{message}</li>
        )}
        </ul>
    </>
}

export default ActionLog