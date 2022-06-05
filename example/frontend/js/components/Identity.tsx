import * as React from 'react';
import { useEffect } from 'react'
import { useState } from "@hookstate/core";

import { useEvent } from "../livearea/events/hooks";
import { EventTypes } from "../livearea/events/entities";
import { sessionID } from "../states/sessions";

import "./Identity.css"

const Identity = (): JSX.Element => {
    const sessionId = useState(sessionID)

    useEvent(EventTypes.document_opened, ({session_id}) => {
        sessionId.set(session_id)
    })

    return <div className={`identity`}>
        <h3>🔐 Your Identity</h3>
        <p>Session ID: <strong>{sessionId.get()}</strong></p>
    </div>
}

export default Identity