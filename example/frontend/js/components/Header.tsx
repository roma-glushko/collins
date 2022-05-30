import * as React from "react";

import "./Header.css"

type HeaderProps = {
    children?: JSX.Element | JSX.Element[]
}

const Header = (props: HeaderProps): JSX.Element => (
    <header>
        <h1>
            📻 Live Area
            <div className="live" />
        </h1>
        <p>Example of real-time collaboration based on the Operational Transformation algorithm</p>
        {props.children}
    </header>
)

export default Header