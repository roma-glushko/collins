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

export interface CommitChangesData {
    base_revision: number;
    changeset: string;
}

export interface ServerEvents {
    document_opened: DocumentOpenedData,
    document_joined: DocumentJoinedData,
    document_left: DocumentLeftData,
}

export interface ClientEvents {
    commit_changes: CommitChangesData
}

export enum EventTypes {
    document_opened = "document_opened",
    document_joined = "document_joined",
    document_left = "document_left",

    commit_changes = "commit_changes",
}

export interface Events extends ServerEvents, ClientEvents {}

export interface Message<T extends Events> {
    type: keyof T;
    data: T[keyof T];
}