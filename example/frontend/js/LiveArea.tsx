import * as React from "react";

import { createRoot } from 'react-dom/client';

import Textarea from "./components/Textarea";
import ActionLog from "./components/ActionLog";
import AppInfo, { sessionID } from "./components/AppInfo";
import { Websocket } from "./components/Websocket";

const LiveArea = (): JSX.Element => (
    <>
        <AppInfo />
        <Textarea />
        <ActionLog />
        <Websocket sessionID={sessionID.get()} />
    </>
)

const container = document.getElementById('live-area-app');
const root = createRoot(container!);

root.render(<LiveArea />);