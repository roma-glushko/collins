import * as React from 'react';

import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import {State, useState} from "@hookstate/core";


const OtherViewers = (): JSX.Element => {
    const otherViewers: State<string[]> = useState([] as string[])

    useEvent(EventTypes.document_opened, ({other_viewers}) => {
        otherViewers.set(other_viewers || [])
    })

    useEvent(EventTypes.document_joined, ({session_id}) => {
        otherViewers.merge([session_id])
    })

    useEvent(EventTypes.document_left, ({session_id}) => {
        otherViewers.set(
            otherViewers.get().filter(
                (viewerID: string) => viewerID !== session_id
            )
        )
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