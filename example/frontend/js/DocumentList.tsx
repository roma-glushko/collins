import * as React from "react";

import { createRoot } from 'react-dom/client';

import Header from "./components/Header";
import Footer from "./components/Footer";
import DocumentList from "./components/DocumentList";

import "./common.css"
import "./DocumentList.css"


const DocumentListing = (): JSX.Element => (
    <>
        <Header>
            <h2>Available Documents</h2>
        </Header>
        <DocumentList />
        <Footer />
    </>
)

const container = document.getElementById('live-area-app');
const root = createRoot(container!);

root.render(<DocumentListing />);