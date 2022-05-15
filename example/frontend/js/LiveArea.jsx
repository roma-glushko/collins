import React from "react";
import ReactDOM from "react-dom";

import Textarea from "./components/Textarea";

const LiveArea = () => {
    return <Textarea />;
};

ReactDOM.render(
    <LiveArea />,
    document.getElementById("live-area-app")
);