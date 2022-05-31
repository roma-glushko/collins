import * as React from 'react';
import { useEffect } from 'react'
import { createState, State } from '@hookstate/core';
import { uuid } from "../utils";

export const sessionID: State<string> = createState(uuid());

const AppInfo = (): JSX.Element => {
    useEffect(() => {
        const prevTitle: string = document.title;
        document.title += ` (${sessionID.get()})`;

        return () => {
          document.title = prevTitle;
        };
    });

    return <>
        <h3>Your ID: <span>{sessionID.get()}</span></h3>
    </>
}

export default AppInfo