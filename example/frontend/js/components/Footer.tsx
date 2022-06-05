import * as React from "react";

import "./Footer.css"

type FooterProps = {
    children?: JSX.Element | JSX.Element[]
}

const Footer = (props: FooterProps): JSX.Element => (
    <footer>
        Made with ❤️ and 🫖 by <a target={`_blank`} href={"https://github.com/roma-glushko"}>@roma_glushko</a>
        {props.children}
    </footer>
)

export default Footer