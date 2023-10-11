def _kern_octave(pitch: int, letter: str, tet: int = 12) -> str:
    octave = pitch // tet - 5
    if octave >= 0:
        return letter.lower() * (octave + 1)
    return letter.upper() * (-octave)


def shell_spelling_to_humdrum_spelling(
    shell_pc: str, pitch: int, tet: int = 12, input_flat_sign: str = "b"
) -> str:
    """
    >>> shell_spelling_to_humdrum_spelling("C", 36)
    'CC'
    >>> shell_spelling_to_humdrum_spelling("C", 48)
    'C'
    >>> shell_spelling_to_humdrum_spelling("C", 60)
    'c'
    >>> shell_spelling_to_humdrum_spelling("C", 72)
    'cc'
    >>> shell_spelling_to_humdrum_spelling("B#", 72)
    'b#'
    >>> shell_spelling_to_humdrum_spelling("Cb", 71)
    'cc-'
    >>> shell_spelling_to_humdrum_spelling("Dbbb", 71)
    'dd---'
    >>> shell_spelling_to_humdrum_spelling("A###", 72)
    'a###'
    """
    alteration = shell_pc.count("#") - shell_pc.count(input_flat_sign)
    return _kern_octave(pitch - alteration, shell_pc[0], tet=tet) + shell_pc[
        1:
    ].replace(input_flat_sign, "-")
