from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, get_db, wait_for_db
from models import Answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="stats-service", version="0.1.0", lifespan=lifespan)


class AnswerIn(BaseModel):
    exercise_id: str
    clef: str
    note_key: str
    note_letter: str
    given_answer: str
    correct: bool
    response_time_ms: Optional[int] = None


class AnswerOut(AnswerIn):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/answers", response_model=AnswerOut)
def record_answer(answer: AnswerIn, db: Session = Depends(get_db)):
    row = Answer(**answer.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.get("/summary")
def stats_summary(db: Session = Depends(get_db)):
    answers = db.query(Answer).order_by(Answer.created_at).all()
    total = len(answers)
    correct_count = sum(1 for a in answers if a.correct)

    by_letter: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "correct": 0})
    for a in answers:
        by_letter[a.note_letter]["total"] += 1
        if a.correct:
            by_letter[a.note_letter]["correct"] += 1

    accuracy_by_note = {
        letter: round(100 * counts["correct"] / counts["total"], 1)
        for letter, counts in by_letter.items()
    }

    current_streak = 0
    for a in reversed(answers):
        if a.correct:
            current_streak += 1
        else:
            break

    best_streak = 0
    running = 0
    for a in answers:
        running = running + 1 if a.correct else 0
        best_streak = max(best_streak, running)

    return {
        "total_answers": total,
        "correct_answers": correct_count,
        "accuracy": round(100 * correct_count / total, 1) if total else 0,
        "accuracy_by_note": accuracy_by_note,
        "current_streak": current_streak,
        "best_streak": best_streak,
    }