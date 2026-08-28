from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(String, index=True)
    clef = Column(String, nullable=False)
    note_key = Column(String, nullable=False)
    note_letter = Column(String, nullable=False)
    given_answer = Column(String, nullable=False)
    correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())