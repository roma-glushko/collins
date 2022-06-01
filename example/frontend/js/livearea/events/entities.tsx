import { Document } from "../documents"

export interface DocumentOpenedData {
    session_id: string
    document: Document
    other_viewers: string[]
}

export interface DocumentJoinedData {
    session_id: string
}

export interface DocumentLeftData {
    session_id: string
}

export interface ServerEvents {
    document_opened: DocumentOpenedData,
    document_joined: DocumentJoinedData,
    document_left: DocumentLeftData,
}

export interface ClientEvents {

}

export enum EventTypes {
    document_opened = "document_opened",
    document_joined = "document_joined",
    document_left = "document_left",
}

export interface Events extends ServerEvents, ClientEvents {}

export interface Message<T extends Events> {
    type: keyof T;
    data: T[keyof T];
}