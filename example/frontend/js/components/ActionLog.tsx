import * as React from 'react';
import {State, useState} from "@hookstate/core";

import {useEvent} from "../livearea/events/hooks";
import {EventTypes} from "../livearea/events/entities";

import "./ActionLog.css"

const ActionLog = (): JSX.Element => {
    const logs: State<string[]> = useState([]) as State<string[]>;

    useEvent(EventTypes.document_opened, ({document}) => {
        logs.merge([`Document "${document.title}" has been opened (rev: ${document.revision_id})`])
    })

    useEvent(EventTypes.document_joined, ({session_id}) => {
        logs.merge([`Viewer ${session_id} has joined the document`])
    })

    useEvent(EventTypes.document_left, ({session_id}) => {
        logs.merge([`Viewer ${session_id} has left the document`])
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