import * as React from "react";

import { createRoot } from 'react-dom/client';

import Header from "./components/Header";
import Textarea from "./components/Textarea";
import ActionLog from "./components/ActionLog";
import Identity from "./components/Identity";
import { Websocket } from "./components/Websocket";
import Footer from "./components/Footer";
import OtherViewers from "./components/OtherViewers";


import "./common.css"
import "./DocumentView.css"


const DocumentView = (): JSX.Element => (
    <>
        <Header>
            <>
                <a href={`/`}>all documents</a>
            </>
        </Header>
        <Identity />
        <div className={`document-view`}>
            <Textarea />
            <div className={`sidebar`}>
                <OtherViewers />
                <ActionLog />
            </div>
            <Websocket />
        </div>
        <Footer />
    </>
)

const container = document.getElementById('livearea-app');
const root = createRoot(container!);

root.render(<DocumentView />);