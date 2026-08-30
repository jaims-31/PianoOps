import uuid
from typing import Literal

from fastapi import FastAPI, Query
from notes import NOTE_LABELS, random_note

app = FastAPI(title="exercises-service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/exercise")
def get_exercise(
    clef: Literal["treble", "bass"] = Query(
        "treble", description="Clé de sol ou de fa"
    ),
    difficulty: int = Query(
        1, ge=1, le=3, description="1 = facile, 3 = avec altérations"
    ),
):
    note = random_note(clef, difficulty)
    return {
        "id": str(uuid.uuid4()),
        "clef": note["clef"],
        "key": note["key"],
        "answer_options": NOTE_LABELS,
    }
