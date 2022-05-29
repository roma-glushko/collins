import * as React from 'react';

import {useState} from "@hookstate/core";

import "./DocumentList.css"

const fetchDocumentList = () => {
    return fetch("http://localhost:3003/api/documents/")
        .then(response => response.json())
}

const cutDescription = (description: string, max_length: number = 150): string => {
    let excerpt = description.substring(0, max_length);
      excerpt = excerpt.substring(0, excerpt.lastIndexOf(' '));

      return `${excerpt}...`
}

const DocumentList = (): JSX.Element => {
    const state = useState(fetchDocumentList);

    if (state.promised) {
        return <p>Loading documents..</p>;
    }

    return <ul className={`document-list`}>
        { state.get().map((document) => (
        <li key={document.id}>
            <a href={`http://localhost:3003/documents/${document.id}/`}>
                <h3>{document.title}</h3>
                <p>{cutDescription(document.body)}</p>
            </a>
        </li>
        )}
    </ul>
}

export default DocumentList