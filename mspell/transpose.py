from collections import defaultdict
from typing import Iterable

SPELLED_TO_IDX = defaultdict(dict)
IDX_TO_SPELLED = defaultdict(list)

alphabet = "FCGDAEB"


def _init_pitch_cache(flat_char):
    for i in range(513):
        accidental_i, letter_i = divmod(i - 256, 7)
        spelled = f"{alphabet[letter_i]}{(flat_char if accidental_i < 0 else '#') * abs(accidental_i)}"
        SPELLED_TO_IDX[flat_char][spelled] = i
        IDX_TO_SPELLED[flat_char].append(spelled)


def transpose_spelling(
    spelled_pitches: Iterable[str],
    chromatic_steps: int,
    diatonic_steps: int,
    letter_format: str = "shell",
    flat_char: str = "b",
) -> list[str]:
    """
    >>> transpose_spelling(["C", "E", "G"], 1, 1)
    ['Db', 'F', 'Ab']
    >>> transpose_spelling(["C", "E", "G"], 1, 0)
    ['C#', 'E#', 'G#']
    >>> transpose_spelling(["C", "E", "G"], 7, 4)
    ['G', 'B', 'D']
    >>> transpose_spelling(["C", "E", "G"], -5, -3)
    ['G', 'B', 'D']
    >>> transpose_spelling(["C", "E", "G"], -6, -3)
    ['Gb', 'Bb', 'Db']
    >>> transpose_spelling(["C", "E", "G"], -2, -1)
    ['Bb', 'D', 'F']
    """

    if letter_format != "shell":
        raise NotImplementedError

    fifths = -12 * diatonic_steps + 7 * chromatic_steps
    if not SPELLED_TO_IDX[flat_char]:
        _init_pitch_cache(flat_char)
    out = [
        IDX_TO_SPELLED[flat_char][SPELLED_TO_IDX[flat_char][p] + fifths]
        for p in spelled_pitches
    ]
    return out
