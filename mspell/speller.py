from numbers import Number
from typing import Optional, Sequence, Union

import numpy as np


from .spell_base import SingleSpellBase
from . import utils


ALPHABET = "fcgdaeb"


class Speller(SingleSpellBase):
    """Spells pitches or pitch-classes in specified temperament.

    When spelling pitches, C4 is always 5 * t, where t is the cardinality of the
    temperament. So in 12-tet, C4 = 5 * 12 = 60; in 31-tet, C4 = 5 * 31 = 155,
    and so on.

    Double-sharps and flats (and bselselfeyond) are always indicated by repetition of
    the accidental symbol (e.g., F##).

    Keyword args:
        tet: integer. Default 12.
        pitches: boolean. If true, spells pitches by default (e.g., in 12-tet,
            60 = "C4"; note the octave number). If false, spells pitch-classes
            by default (e.g., in 12-tet, 60 = "C").
            Default: False.
        rests: boolean. If true, spells None as "Rest" (if letter_format is
            "shell") or "r" (if letter_format is "kern"). If false, raises a
            TypeError on None values.
        letter_format: string.
            Possible values:
                "shell": e.g., "C4", "Ab2", "F#7"
                "kern": e.g., "c", "DD", "b-", "F#"

    Raises:
        ValueError: if letter_format is not "shell" or "kern".
        ValueError: if gcd(tet, utils.approximate_just_interval(3/2, tet))
            is not 1.

    Methods:
         __call__(item, pitches=None)
    """

    def __init__(
        self,
        tet: int = 12,
        pitches: bool = False,
        rests: bool = True,
        letter_format: str = "shell",
    ):
        self._tet = tet
        self._pitches = pitches
        self._rests = rests
        self._letter_format = letter_format
        if letter_format == "shell":
            self._pitch = self._shell_pitch
            self._rest_str = "Rest"
        elif letter_format == "kern":
            self._pitch = self._kern_pitch
            self._rest_str = "r"
        else:
            raise ValueError(
                f"letter_format {letter_format} not in ('shell', 'kern')"
            )

    def _shell_pitch(self, pc_string: str, pitch_num: int) -> str:
        """Appends an octave number to a pitch-class (e.g., "C#" becomes "C#3")"""
        octave = pitch_num // self.tet - 1 + self.octave_offsets[pitch_num % self.tet]
        return pc_string + str(octave)

    def _kern_pitch(self, pc_string: str, pitch_num: int) -> str:
        if pc_string[0] == "c" and pc_string[-1] == "-":
            pitch_num += self.tet
        temp_num = (pitch_num % self.tet) + (self.tet * 5)

        if temp_num > pitch_num:
            pc_string = pc_string[0].upper() + pc_string[1:]
            temp_num -= self.tet
        while temp_num > pitch_num:
            pc_string = pc_string[0] + pc_string
            temp_num -= self.tet
        while temp_num < pitch_num:
            pc_string = pc_string[0] + pc_string
            temp_num += self.tet

        return pc_string

    @utils.nested_method(coerce_to_list=True)
    def __call__(
        self, item: Union[int, Sequence], pitches: Optional[bool] = None
    ) -> Union[str, Sequence[str]]:
        """Spells integers as musical pitches or pitch-classes.

        Args:
            item: either an integer, or an (arbitrarily deep and nested)
                list-like of integers (and None values, if Speller was
                initialized with rests=True). If non-integer numbers are
                passed, they will be cast to ints with int().

        Keyword args:
            pitches: boolean. Overrides the default setting for
                the Speller instance. If true, spells pitches (e.g., in 12-tet,
                60 = "C4"). If false, spells pitch-classes (e.g., in 12-tet,
                60 = "C").
                Default: None.

        Returns:
            A string representing a single pitch, if item is an integer.
            A list of strings, if item is a list-like, with the same depth and
                nesting as item.

        Raises:
            TypeError if iter() fails on item and item is not a number (or
                None, if Speller was initialized with rests=True.)
        """
        if pitches is None:
            pitches = self._pitches

        if not isinstance(item, Number):
            if item is not None and self._rests:
                raise TypeError(
                    "Speller() can only take iterables of "
                    "integers, or None for rests"
                )
            elif not self._rests:
                raise TypeError(
                    "Speller() with rests=False can only take "
                    "iterables of integers"
                )

        if item is None:
            return self._rest_str

        if item < 0:
            return item

        if not isinstance(item, int):
            item = int(item)

        pitch_class = self.spell_dict[item % self.tet]
        if not pitches:
            return pitch_class

        return self._pitch(pitch_class, item)

    # Not sure if or why this function would be needed
    # def spelled_string(self, item, pitches=None):
    #     if isinstance(item, typing.Sequence) and not isinstance(item, str):
    #         flat = list(flatten(item))
    #         if any([isinstance(f, str) for f in flat]):
    #             if not all([isinstance(f, str) for f in flat]):
    #                 raise TypeError
    #             return " ".join(flat)
    #         return " ".join(self.spelled_list(flat, pitches=pitches))

    #     if isinstance(item, str):
    #         return item
    #     return self.spelled_list(item, pitches=pitches)
