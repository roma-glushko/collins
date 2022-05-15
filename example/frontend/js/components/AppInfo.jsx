import React, { useEffect } from 'react';
import { createState, useState } from '@hookstate/core';

const uuid = () => URL.createObjectURL(new Blob([])).substring(36)

const sessionID = createState(uuid());

const AppInfo = () => {
    useEffect(() => {
        const prevTitle = document.title;
        document.title += ` (${sessionID.get()})`;

        return () => {
          document.title = prevTitle;
        };
    });

    return <>
        <h1>📻 Live Area</h1>
        <p>Example of real-time collaboration based on the Operational Transformation algorithm</p>
        <h3>Your ID: <span>{sessionID.get()}</span></h3>
    </>
}

export default AppInfo