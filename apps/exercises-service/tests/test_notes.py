import pytest
from notes import NOTE_POOLS, letter_of, random_note


def test_letter_of_extracts_note_name_without_accidental_or_octave():
    assert letter_of("c/4") == "c"
    assert letter_of("f#/2") == "f"
    assert letter_of("g#/5") == "g"


@pytest.mark.parametrize("clef", ["treble", "bass"])
@pytest.mark.parametrize("difficulty", [1, 2, 3])
def test_random_note_stays_within_expected_pool(clef, difficulty):
    for _ in range(50):
        note = random_note(clef, difficulty)
        assert note["clef"] == clef
        assert note["key"] in NOTE_POOLS[clef][difficulty]
        assert note["letter"] == note["key"][0].upper()


@pytest.mark.parametrize(
    "raw_difficulty,expected_level",
    [(0, 1), (-5, 1), (1, 1), (4, 3), (99, 3)],
)
def test_random_note_clamps_out_of_range_difficulty(raw_difficulty, expected_level):
    note = random_note("treble", raw_difficulty)
    assert note["key"] in NOTE_POOLS["treble"][expected_level]
