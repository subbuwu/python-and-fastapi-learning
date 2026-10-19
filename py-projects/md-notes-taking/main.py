from contextlib import asynccontextmanager
from uuid import uuid4
from pathlib import Path
from fastapi import FastAPI,UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from db import get_connection, initialize_database
from models.notes import MarkdownNote, GrammarCheckRequest
import markdown
import httpx


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

@app.get("/notes/{note_id}")
def get_notes_by_id(note_id : str):
    with get_connection() as conn:
        row = conn.execute(
        """
        SELECT * from notes where id = ?
        """
        ,(note_id,)
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

@app.get("/notes/{note_id}/html", response_class=HTMLResponse)
def render_notes_html(note_id : str):
    with get_connection() as conn:
        row = conn.execute(
        """
        SELECT * from notes WHERE id = ?
        """,
        (note_id,)
        ).fetchone()
        
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
    )
        
    row = dict(row)
    html = markdown.markdown(
        row["content"],
        extensions=["fenced_code", "tables"]
    )
    return HTMLResponse(html)

@app.post("/notes/check-grammar")
async def check_grammar_notes(request: GrammarCheckRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.languagetool.org/v2/check",
                data={
                    "text": text,
                    "language": "en-US"
                }
            )

            response.raise_for_status()
            result = response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Grammar checking service is unavailable"
        )

    issues = []

    for match in result.get("matches", []):
        offset = match["offset"]
        length = match["length"]

        issues.append({
            "message": match["message"],
            "incorrect_text": text[offset:offset + length],
            "offset": offset,
            "length": length,
            "suggestions": [
                replacement["value"]
                for replacement in match.get("replacements", [])
            ]
        })

    return {
        "original_text": text,
        "issue_count": len(issues),
        "issues": issues
    }