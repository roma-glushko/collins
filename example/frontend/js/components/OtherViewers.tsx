import * as React from 'react';

import {State, useState} from "@hookstate/core";

import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import { getRandomColor } from "./colors";

import "./OtherViewers.css"

interface Viewer {
    session_id: string;
    color: string;
}

const createViewerList = (sessionIDs: string[]): Viewer[] => {
    return sessionIDs.map((session_id) => {
        return {
            session_id: session_id,
            color: getRandomColor(),
        }
    })
}

const OtherViewers = (): JSX.Element => {
    const otherViewers: State<Viewer[]> = useState([] as Viewer[])

    useEvent(EventTypes.document_opened, ({other_viewers}) => {
        otherViewers.set(createViewerList(other_viewers) || [])
    })

    useEvent(EventTypes.document_joined, (data) => {
        otherViewers.merge([{session_id: data.session_id, color: getRandomColor()}])
    })

    useEvent(EventTypes.document_left, (data) => {
        otherViewers.set(
            otherViewers.get().filter(
                (viewer: Viewer) => viewer.session_id !== data.session_id
            )
        )
    })

    if (!otherViewers.length) {
        return <></>
    }

    return <div className={`other-viewers`}>
        <h3>Other Viewers</h3>
        <ul>
            {otherViewers.get().map((viewer: Viewer) => (
                <li key={viewer.session_id}>
                    <div title={viewer.session_id} className="viewerAvatar" style={{backgroundColor: viewer.color}}>
                        <span>{viewer.session_id.substring(0, 2)}</span>
                    </div>
                </li>
            ))}
        </ul>
    </div>
}

export default OtherViewers