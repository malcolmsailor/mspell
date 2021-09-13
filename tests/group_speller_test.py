import mspell


def test_group_speller():
    tests = [
        (1, 4, 9),
        (),
        (2,),
        (3,),
        (1,),
        (0, 3, 8),
        (1, 3, 4, 6, 8, 9, 11),
        (0, 1, 3, 5, 6, 8, 10),
        (0, 2, 3, 5, 7, 9, 11),
        (0, 1, 3, 4, 6, 8, 10),
        (0, 2, 3, 5, 6, 8, 10),
        (1, 9, 4, 1, 4, 9, 4, 9, 1),
    ]
    results = [
        ["C#", "E", "A"],
        [],
        ["D"],
        ["Eb"],
        ["C#"],
        ["C", "Eb", "Ab"],
        ["C#", "D#", "E", "F#", "G#", "A", "B"],
        ["C", "Db", "Eb", "F", "Gb", "Ab", "Bb"],
        ["C", "D", "Eb", "F", "G", "A", "B"],
        ["B#", "C#", "D#", "E", "F#", "G#", "A#"],
        ["C", "D", "Eb", "F", "Gb", "Ab", "Bb"],
        ["C#", "A", "E", "C#", "E", "A", "E", "A", "C#"],
    ]
    group_speller = mspell.GroupSpeller()
    kern_speller = mspell.GroupSpeller(letter_format="kern")
    for test, result in zip(tests, results):
        assert (
            list(group_speller(test)) == result
        ), "list(group_speller(test)) != result"
    tests = [
        ((60, 63, 66), ("C4", "Eb4", "Gb4"), ("c", "e-", "g-")),
        ((24, 48, 60, 71), ("C1", "C3", "C4", "B4"), ("CCC", "C", "c", "b")),
    ]
    for (test, shell, kern) in tests:
        assert group_speller.pitches(test) == list(
            shell
        ), "group_speller.pitches(test) != list(shell)"
        assert kern_speller.pitches(test) == list(
            kern
        ), 'group_speller.pitches(test, letter_format="kern") != list(kern)'
    tests = [
        ((60, 63, None, 66), ("C4", "Eb4", "", "Gb4"), ("c", "e-", "r", "g-")),
        (
            (24, None, 48, 60, 71, None),
            ("C1", "", "C3", "C4", "B4", ""),
            ("CCC", "r", "C", "c", "b", "r"),
        ),
    ]
    for (test, shell, kern) in tests:
        assert group_speller.pitches(test, rests="") == list(shell), (
            "group_speller.pitches(test, rests=" ") != list(shell)"
        )
        assert kern_speller.pitches(test, rests="r") == list(
            kern
        ), 'group_speller.pitches(test, letter_format="kern", rests="r") != list(kern)'

    for tet, minor_triad in zip(
        (12, 19, 31), ((0, 3, 7), (0, 5, 11), (0, 8, 18))
    ):
        spell_unspell_onespell_pcs = (
            (
                mspell.GroupSpeller(
                    tet=tet, pitches=False, letter_format="shell"
                ),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="shell"),
                mspell.Speller(tet=tet, pitches=False, letter_format="shell"),
            ),
            (
                mspell.GroupSpeller(
                    tet=tet, pitches=False, letter_format="kern"
                ),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="kern"),
                mspell.Speller(tet=tet, pitches=False, letter_format="kern"),
            ),
        )
        for spell, unspell, onespell in spell_unspell_onespell_pcs:
            for i in range(tet * 2):
                assert spell([i])[0] == onespell(i)
                chord = [(p + i) % tet for p in minor_triad]
                assert unspell(spell(chord)) == chord
