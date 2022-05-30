import * as React from "react";

import { createRoot } from 'react-dom/client';

import Header from "./components/Header";
import Textarea from "./components/Textarea";
import ActionLog from "./components/ActionLog";
import AppInfo, { sessionID } from "./components/AppInfo";
import { Websocket } from "./components/Websocket";
import Footer from "./components/Footer";


import "./common.css"
import "./DocumentView.css"
import {documentID} from "./states/documentID";


const DocumentView = (): JSX.Element => (
    <>
        <Header>
            <>
                <h3>
                    <a href={`/`}>all documents</a>
                </h3>
                <AppInfo />
            </>
        </Header>
        <div className={`document-view`}>
            <Textarea />
            <ActionLog />
            <Websocket documentID={documentID.get()} sessionID={sessionID.get()} />
        </div>
        <Footer />
    </>
)

const container = document.getElementById('livearea-app');
const root = createRoot(container!);

root.render(<DocumentView />);