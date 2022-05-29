import * as React from "react";

import "./Header.css"

const Header = ({children}): JSX.Element => (
    <header>
        <h1>
            📻 Live Area
            <div className="live" />
        </h1>
        <p>Example of real-time collaboration based on the Operational Transformation algorithm</p>
        {children}
    </header>
)

export default Header