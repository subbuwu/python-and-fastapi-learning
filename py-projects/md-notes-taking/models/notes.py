
from pydantic import BaseModel, Field


class MarkdownNote(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str


class MarkdownNoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None
class GrammarCheckRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)