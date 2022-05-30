import * as React from 'react';
import { receivedMessages } from "./Websocket";
import { useState } from "@hookstate/core";

import "./ActionLog.css"

const ActionLog = () => {
    const messages = useState(receivedMessages);

    return <div className={`action-log`}>
        <h3>Action Log</h3>
        <ul id="actions">
        {messages.get().map((message: string, messageIndex: number) =>
            <li key={messageIndex}>{message}</li>
        )}
        </ul>
    </div>
}

export default ActionLog