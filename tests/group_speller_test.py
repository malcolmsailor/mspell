import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from mspell import GroupSpeller


def test_build_fifth_class_spelling_dict():
    spell_dict = GroupSpeller.build_fifth_class_spelling_dict()
    spell_dict2 = GroupSpeller.build_fifth_class_spelling_dict(forward=False)
    kern_dict = GroupSpeller.build_fifth_class_spelling_dict(
        letter_format="kern"
    )
    for pc, spelled in spell_dict.items():
        assert spell_dict2[spelled] == pc, "spell_dict2[spelled] != pc"
    tests = [
        (0, "D", "d"),
        (7, "D#", "d#"),
        (-7, "Db", "d-"),
        (3, "B", "b"),
        (17, "B##", "b##"),
        (-11, "Bbb", "b--"),
    ]
    for pc, shell_spelled, kern_spelled in tests:
        assert (
            spell_dict[pc] == shell_spelled
        ), "spell_dict[pc] != shell_spelled"
        assert kern_dict[pc] == kern_spelled, "kern_dict[pc] != kern_spelled"


def test_group_speller():
    tests = [
        (),
        (2,),
        (3,),
        (1,),
        (1, 4, 9),
        (0, 3, 8),
        (1, 3, 4, 6, 8, 9, 11),
        (0, 1, 3, 5, 6, 8, 10),
        (0, 2, 3, 5, 7, 9, 11),
        (0, 1, 3, 4, 6, 8, 10),
        (0, 2, 3, 5, 6, 8, 10),
        (1, 9, 4, 1, 4, 9, 4, 9, 1),
    ]
    results = [
        [],
        ["D"],
        ["Eb"],
        ["C#"],
        ["C#", "E", "A"],
        ["C", "Eb", "Ab"],
        ["C#", "D#", "E", "F#", "G#", "A", "B"],
        ["C", "Db", "Eb", "F", "Gb", "Ab", "Bb"],
        ["C", "D", "Eb", "F", "G", "A", "B"],
        ["B#", "C#", "D#", "E", "F#", "G#", "A#"],
        ["C", "D", "Eb", "F", "Gb", "Ab", "Bb"],
        ["C#", "A", "E", "C#", "E", "A", "E", "A", "C#"],
    ]
    group_speller = GroupSpeller()
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
        assert group_speller.pitches(test, letter_format="kern") == list(
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
        assert group_speller.pitches(
            test, letter_format="kern", rests="r"
        ) == list(
            kern
        ), 'group_speller.pitches(test, letter_format="kern", rests="r") != list(kern)'
