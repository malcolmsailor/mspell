import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# import mspell.speller as speller
# import mspell.unspeller as unspeller
import mspell


def test_speller_pcs():
    for tet in (12, 19, 31):
        forward_backward = (
            (
                mspell.Speller(tet=tet, pitches=False, letter_format="shell"),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="shell"),
            ),
            (
                mspell.Speller(tet=tet, pitches=False, letter_format="kern"),
                mspell.Unspeller(tet=tet, pitches=False, letter_format="kern"),
            ),
        )
        for forward, backward in forward_backward:
            for pc, spelled in forward._spelling_dict.items():
                assert backward._pc_dict[spelled] == pc

    shell_speller = mspell.Speller(pitches=False)
    kern_speller = mspell.Speller(pitches=False, letter_format="kern")
    tests = [
        (0, "C", "c"),
        (5, "F", "f"),
        (3, "Eb", "e-"),
        (1, "C#", "c#"),
    ]
    for pc, shell_spelled, kern_spelled in tests:
        assert shell_speller(pc) == shell_spelled
        assert kern_speller(pc) == kern_spelled


def test_speller():
    sp = mspell.Speller(pitches=True)
    assert sp(60) == "C4", "sp(60) " '!= "C4"'


if __name__ == "__main__":
    test_speller_pcs()
    test_speller()
