from mspell.spell_base import SpellBase


def test_get_spell_dict():
    for tet in (12, 19, 31):
        spell_dict = SpellBase._get_spell_dict(
            tet, letter_format="shell", forward=True
        )
        spell_dict2 = SpellBase._get_spell_dict(
            tet, letter_format="shell", forward=False
        )
        for pc, spelled in spell_dict.items():
            assert spell_dict2[spelled] == pc, "spell_dict2[spelled] != pc"
    spell_dict = SpellBase._get_spell_dict(
        12, letter_format="shell", forward=True
    )
    kern_dict = SpellBase._get_spell_dict(
        12, letter_format="kern", forward=True
    )
    tests = [
        (0, "C", "c"),
        (5, "F", "f"),
        (3, "Eb", "e-"),
        (1, "C#", "c#"),
    ]
    for pc, shell_spelled, kern_spelled in tests:
        assert (
            spell_dict[pc] == shell_spelled
        ), "spell_dict[pc] != shell_spelled"
        assert kern_dict[pc] == kern_spelled, "kern_dict[pc] != kern_spelled"
