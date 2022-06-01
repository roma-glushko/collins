import * as React from 'react';

import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import {State, useState} from "@hookstate/core";


const OtherViewers = (): JSX.Element => {
    const otherViewers: State<string[]> = useState([] as string[])

    useEvent(EventTypes.document_joined, (data) => {
        otherViewers.merge([data.session_id])
    })

    useEvent(EventTypes.document_left, (data) => {
        // TODO:
    })

    if (!otherViewers.length) {
        return <></>
    }

    return <div className={`other-viewers`}>
        <h3>Other Viewers</h3>
        <ul>
            {otherViewers.get().map((viewerID: string) => (
                <li>{viewerID}</li>
            ))}
        </ul>
    </div>
}

export default OtherViewers