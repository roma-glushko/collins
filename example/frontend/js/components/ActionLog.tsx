import * as React from 'react';
import {State, useState} from "@hookstate/core";

import {useEvent} from "../livearea/events/hooks";
import {EventTypes} from "../livearea/events/entities";

import "./ActionLog.css"

const ActionLog = (): JSX.Element => {
    const logs: State<string[]> = useState([]) as State<string[]>;

    useEvent(EventTypes.document_opened, (data) => {
        logs.merge([`Document "${data.document.title}" has been opened`])
    })

    useEvent(EventTypes.document_joined, (data) => {
        logs.merge([`Viewer ${data.session_id} has joined the document`])
    })

    useEvent(EventTypes.document_left, (data) => {
        logs.merge([`Viewer ${data.session_id} has left the document`])
    })

    return <div className={`action-log`}>
        <h3>Action Log</h3>
        <ul className={`actions`}>
        {logs.get().map((log: string, logIdx: number) =>
            <li key={logIdx}>{log}</li>
        )}
        </ul>
    </div>
}

export default ActionLog