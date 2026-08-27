"""Génération de notes aléatoires pour les exercices de lecture de partition.

Les clés de note suivent le format VexFlow ("note/octave", ex: "c/4" = do
central), ce qui permet au frontend de les passer telles quelles au moteur
de rendu de la portée sans recalcul côté client.
"""

import random
from typing import Literal

Clef = Literal["treble", "bass"]

# Plages de notes par clé et par niveau de difficulté.
# Niveau 1 : notes sur la portée uniquement (pas de ligne supplémentaire).
# Niveau 2 : on ajoute quelques lignes supplémentaires de part et d'autre.
# Niveau 3 : on ajoute des altérations (dièses).
NOTE_POOLS: dict[str, dict[int, list[str]]] = {
    "treble": {
        1: ["e/4", "f/4", "g/4", "a/4", "b/4", "c/5", "d/5", "e/5", "f/5"],
        2: [
            "c/4", "d/4", "e/4", "f/4", "g/4", "a/4", "b/4",
            "c/5", "d/5", "e/5", "f/5", "g/5", "a/5",
        ],
        3: [
            "c/4", "c#/4", "d/4", "d#/4", "e/4", "f/4", "f#/4", "g/4", "g#/4",
            "a/4", "a#/4", "b/4",
            "c/5", "c#/5", "d/5", "d#/5", "e/5", "f/5", "f#/5", "g/5", "g#/5", "a/5",
        ],
    },
    "bass": {
        1: ["g/2", "a/2", "b/2", "c/3", "d/3", "e/3", "f/3", "g/3", "a/3"],
        2: [
            "e/2", "f/2", "g/2", "a/2", "b/2",
            "c/3", "d/3", "e/3", "f/3", "g/3", "a/3", "b/3", "c/4",
        ],
        3: [
            "e/2", "f/2", "f#/2", "g/2", "g#/2", "a/2", "a#/2", "b/2",
            "c/3", "c#/3", "d/3", "d#/3", "e/3", "f/3", "f#/3", "g/3", "g#/3",
            "a/3", "a#/3", "b/3", "c/4",
        ],
    },
}

NOTE_LABELS = [
    {"letter": "C", "solfege": "Do"},
    {"letter": "D", "solfege": "Ré"},
    {"letter": "E", "solfege": "Mi"},
    {"letter": "F", "solfege": "Fa"},
    {"letter": "G", "solfege": "Sol"},
    {"letter": "A", "solfege": "La"},
    {"letter": "B", "solfege": "Si"},
]


def letter_of(key: str) -> str:
    """Extrait le nom de note (sans altération ni octave) d'une clé VexFlow.

    Exemple : "f#/4" -> "f".
    """
    return key[0]


def random_note(clef: Clef, difficulty: int) -> dict:
    difficulty = min(max(difficulty, 1), 3)
    pool = NOTE_POOLS[clef][difficulty]
    key = random.choice(pool)
    return {"clef": clef, "key": key, "letter": letter_of(key).upper()}