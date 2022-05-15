const BASE_URL = 'localhost:3003'

const ws = new WebSocket(`ws://${BASE_URL}/ws/${client_id}`);

ws.onmessage = (event) => {
    const messages = document.getElementById("actions")
    const message = document.createElement('li')
    const content = document.createTextNode(event.data)

    message.appendChild(content)
    messages.appendChild(message)
};

const sendMessage = (event) => {
    const input = document.getElementById("messageText")

    ws.send(input.value)

    input.value = ''
    event.preventDefault()
}