import numpy as np

import mspell


def test_speller():
    for tet in (12, 19, 31):
        spell_unspell_pcs = (
            (
                mspell.Speller(tet=tet, pitches=False, letter_format="shell"),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="shell"),
            ),
            (
                mspell.Speller(tet=tet, pitches=False, letter_format="kern"),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="kern"),
            ),
        )
        for spell, unspell in spell_unspell_pcs:
            for i in range(tet * 2):
                assert unspell(spell(i)) == i % tet

        spell_unspell_pitches = (
            (
                mspell.Speller(tet=tet, pitches=True, letter_format="shell"),
                mspell.Unspeller(tet=tet, pitches=True, letter_format="shell"),
            ),
            (
                mspell.Speller(tet=tet, pitches=True, letter_format="kern"),
                mspell.Unspeller(tet=tet, pitches=True, letter_format="kern"),
            ),
        )
        for spell, unspell in spell_unspell_pitches:
            for i in range(tet * 7):
                assert unspell(spell(i)) == i
            for i in range(tet * 3, tet * 5):
                chord = np.array([i, i + 3, i + 7])
                assert np.all(np.equal(unspell(spell(chord)), chord))

    shell_speller = mspell.Speller(pitches=False, rests=True)
    shell_unspeller = mspell.Unspeller(pitches=False, rests=True)
    kern_speller = mspell.Speller(
        pitches=False, letter_format="kern", rests=True
    )
    kern_unspeller = mspell.Unspeller(
        pitches=False, letter_format="kern", rests=True
    )
    tests = [
        (0, "C", "c"),
        (5, "F", "f"),
        (3, "Eb", "e-"),
        (1, "C#", "c#"),
        (None, "Rest", "r"),
    ]
    for pc, shell_spelled, kern_spelled in tests:
        assert shell_speller(pc) == shell_spelled
        assert kern_speller(pc) == kern_spelled
        assert shell_unspeller(shell_spelled) == pc
        assert kern_unspeller(kern_spelled) == pc


if __name__ == "__main__":
    test_speller()
