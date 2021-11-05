import functools

from .spell_base import SingleSpellBase
from . import utils


class Unspeller(SingleSpellBase):
    """Takes spelled pitches or pitch-classes and returns pitch numbers.

    When spelling pitches, C4 is always 5 * c, where c is the cardinality of
    the temperament. So in 12-tet, C4 = 60; in 31-tet, C4 = 155, and so on.

    Expects double-sharps and flats (and beyond) to be indicated by repetition
    of the accidental symbol (e.g., F##).

    Keyword args:
        tet: integer. Default 12.
        pitches: boolean. If true, expects pitches (e.g., in 12-tet, "C4" = 60).
            If false, expects pitch-classes (e.g., in 12-tet, "C" = 0).
            Default: False.
        letter_format: string.
            Possible values:
                "shell": e.g., "C4", "Ab2", "F#7"
                "kern": e.g., "c", "DD", "b-", "F#"

    Raises:
        ValueError: if letter_format is not "shell" or "kern".
        ValueError: if gcd(tet, utils.approximate_just_interval(3/2, tet))
            is not 1.

    Methods:
    # QUESTION where and how to document __call__()?
        unspelled(item, pitches=None)
    """

    def __init__(
        self, tet=12, pitches=False, rests=True, letter_format="shell"
    ):
        self._tet = tet
        self._pitches = pitches
        self._letter_format = letter_format
        if letter_format not in ("shell", "kern"):
            raise ValueError(
                f"letter_format {letter_format} not in ('shell', 'kern')"
            )
        # self._get_letters_and_m2(tet, letter_format)
        # self._pc_dict = self._get_spell_dict(tet, letter_format, forward=False)
        self._rests = rests
        if letter_format == "shell":
            self._unspell = self._unspell_shell
        elif letter_format == "kern":
            self._unspell = self._unspell_kern



    def _unspell_shell(self, item, pitches):
        if self._rests and item == "Rest":
            return None
        letter_pc = self.letter_dict[
            item[0].lower() if self.letter_format == "kern" else item[0].upper()
        ]
        alteration = 0
        for i in range(1, len(item)):
            # we check for "-" on the chance there may be negative octave numbers
            if item[i].isdigit() or item[i] == "-":
                break
            if item[i] == "#":
                alteration += self.m2
            elif item[i] == "b":
                alteration -= self.m2
            else:
                raise ValueError(f"Invalid character {item[i]} in note {item}")
        if not pitches:
            return (letter_pc + alteration) % self.tet
        octave = (int(item[i:]) + 1) * self.tet
        return octave + letter_pc + alteration

    def _unspell_kern(self, item, pitches):
        if self._rests and item == "r":
            return None
        letter = item[0]
        if letter.isupper():
            octave_num = 4
            increment = -1
        else:
            octave_num = 5
            increment = 1
        i = 1
        while i < len(item) and item[i] == letter:
            octave_num += increment
            i += 1
        letter_pc = self.letter_dict[item[0].lower()]
        alteration = 0
        for j in range(i, len(item)):
            if item[i] == "#":
                alteration += self.m2
            elif item[i] == "-":
                alteration -= self.m2
            else:
                raise ValueError(f"Invalid character {item[i]} in note {item}")
        if not pitches:
            return (letter_pc + alteration) % self.tet
        octave = octave_num * self.tet
        return octave + letter_pc + alteration

    def __call__(self, item, pitches=None):
        return self.unspelled(item, pitches=pitches)

    @utils.nested_method()
    def unspelled(self, item, pitches=None):
        """Takes spelled pitch strings, returns integers.

        Args:
            item: either a pitch-string, or an (arbitrarily deep and nested)
                list-like of pitch-strings.

        Keyword args:
            pitches: boolean. Temporarily overrides the current setting for
                the Speller instance. If true, expects pitches (e.g., in 12-tet,
                "C4" = 60). If false, expects pitch-classes (e.g., in 12-tet,
                "C" = 0).
                Default: None.

        Returns:
            An integer, if item is a string.
            A list of integers, if item is a list-like, with the same depth and
                nesting as item.
        """
        if pitches is None:
            pitches = self._pitches

        # MAYBE implement rests?
        # if item == "Rest" and rests:
        #     return None

        return self._unspell(item, pitches=pitches)


if __name__ == "__main__":
    usp = Unspeller(pitches=True)
    # print(usp(["C4", "C5", ["Eb5", "F#4"]], pitches=True, letter_format="kern"))
    print(usp(["C4"]))
    breakpoint()
