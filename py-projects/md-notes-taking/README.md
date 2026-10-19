# Markdown Note-taking API

A note-taking REST API built with Python and FastAPI that allows users to create, manage, upload, and render Markdown notes, with SQLite for persistent storage.

## Features

- Create, retrieve, list, update, and delete notes
- Store note IDs, titles, and Markdown content in SQLite
- Upload Markdown (`.md`) files and save their contents as notes
- Convert Markdown content into HTML
- Check grammar and spelling using the LanguageTool API
- Handle invalid note IDs, file validation errors, and API errors

## Usage

Run the development server:

```bash
uvicorn main:app --reload
```

Explore and test the API using FastAPI's interactive documentation at `/docs`.

## Source

[GitHub Repository](https://github.com/subbuwu/python-and-fastapi-learning/tree/main/py-projects/md-notes-taking)
