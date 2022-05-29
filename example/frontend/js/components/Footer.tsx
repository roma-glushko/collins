import * as React from "react";

const Footer = ({children}): JSX.Element => (
    <footer>
        Made with ❤️ and 🫖 by <a href={"https://github.com/roma-glushko"}>@roma_glushko</a>
        {children}
    </footer>
)

export default Footer