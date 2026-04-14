from typing import Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    concept_description: str
    difficulty: str
    completed: bool = False

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    concept_description: Optional[str] = None
    difficulty: Optional[str] = None
    completed: Optional[bool] = None

class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True
