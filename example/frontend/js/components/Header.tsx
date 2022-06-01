import * as React from "react";

import {useEffect} from "react";
import {useState} from "@hookstate/core";
import {currentDocument} from "../states/documents";

import "./Header.css"

type HeaderProps = {
    children?: JSX.Element | JSX.Element[]
}

const Header = (props: HeaderProps): JSX.Element => {
    const doc = useState(currentDocument)

    useEffect(() => {
        const prevTitle: string = document.title;
        document.title = `${doc.get().title} / ${document.title}`;

        return () => {
          document.title = prevTitle;
        };
    });

    return (
        <header>
            <h1>
                📻 Live Area
                <div className="live"/>
            </h1>
            <p>Example of real-time collaboration based on the Operational Transformation algorithm</p>
            {props.children}
        </header>
    )
}

export default Header