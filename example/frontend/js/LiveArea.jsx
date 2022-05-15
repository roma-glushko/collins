import { createRoot } from 'react-dom/client';

import Textarea from "./components/Textarea";
import ActionLog from "./components/ActionLog";
import AppInfo from "./components/AppInfo";

const LiveArea = () => (
    <>
        <AppInfo />
        <Textarea />
        <ActionLog />
    </>
)

const container = document.getElementById('live-area-app');
const root = createRoot(container);

root.render(<LiveArea />);