from contextlib import asynccontextmanager
from uuid import uuid4
from pathlib import Path
from fastapi import FastAPI,UploadFile, File, HTTPException
from db import get_connection, initialize_database
from models.notes import MarkdownNote, MarkdownNoteUpdate



@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def read_root():
    return {"Markdown Note-taking API"}

@app.post('/notes',status_code=201)
def create_notes(note : MarkdownNote):
        note_id = str(uuid4())
        
        with get_connection() as conn:
            conn.execute(
            """
            INSERT INTO notes (id,title,content)
            VALUES (?, ?, ?)
            """,
            (note_id,note.title,note.content),
        )
        
        return {
            "id" : note_id,
            "title" : note.title,
            "message" : "Note saved successfully"
        }

@app.get("/notes")
def get_notes():
    with get_connection() as conn:
        rows = conn.execute(
        """
        SELECT * from notes ORDER BY created_at DESC , id DESC
        """
        ).fetchall()
    
    return [dict(row) for row in rows]

@app.get("/notes{note_id}")
def get_notes_by_id(note_id : str):
    with get_connection() as conn:
        row = conn.execute(
        """
        SELECT * from notes where id = ?
        """
        ,(note_id),
        ).fetchone()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return dict(row)

@app.post("/notes/upload",status_code=201)
async def upload_markdown_note(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".md":
        raise HTTPException(
            status_code=400,
            detail= "Only markdown (.md) files are allowed"
        )
    
    try:
        file_bytes = await file.read()
        
        try:
            content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="The upload file must use UTF-8 encoding"
        )
            
        title = Path(file.filename).stem
        title = title.replace("_", " ").replace("-", " ").strip()
        
        if not title:
            raise HTTPException(
                status_code=400,
                detail = "The filename must contain a valid title"
        )
        
        note_id = str(uuid4())
        
        with get_connection() as conn:
            conn.execute(
            """
            INSERT INTO notes (id,title,content)
            VALUES (?, ?, ?)
            """,
            (note_id, title, content)
        )
        
        return {
            "id": note_id,
            "title": title,
            "message": "Markdown note uploaded successfully."
        }
    
    finally:
        await file.close()