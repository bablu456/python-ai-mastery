from sqlalchemy import Boolean, Column, Integer, String, Text
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    concept_description = Column(Text)
    difficulty = Column(String) # "Easy", "Medium", "Hard"
    completed = Column(Boolean, default=False)
