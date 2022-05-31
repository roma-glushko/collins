export interface DocumentOpenedData {
    sessionId: string
}

export interface DocumentClosedData {
    sessionId: string
}

export interface ServerEvents {
    document_opened: DocumentOpenedData,
    document_closed: DocumentClosedData,
}

export interface ClientEvents {

}

export interface Events extends ServerEvents, ClientEvents {}

