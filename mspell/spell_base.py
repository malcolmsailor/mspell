import functools
import itertools
import math
from numbers import Number
from typing import Optional

from . import utils

class SpellBase:
    @property
    def tet(self): # pylint: disable=missing-docstring
        return self._tet
    
    @property
    def letter_format(self): # pylint: disable=missing-docstring
        return self._letter_format

    @functools.cached_property
    def flat_sign(self):
        return "-" if self.letter_format == "kern" else "b"

    @functools.cached_property
    def fifth(self):
        tempered_fifth = utils.approximate_just_interval(3 / 2, self.tet)
        if math.gcd(self.tet, tempered_fifth) != 1:
            raise ValueError
        return tempered_fifth

    @functools.cached_property
    def alphabet(self):
        if self.letter_format == "kern":
            return self._alphabet
        return self._alphabet.upper()

class SingleSpellBase(SpellBase):
    _alphabet = "fcgdaeb"

    @functools.cached_property
    def m2(self):
        return (7 * self.fifth) % self.tet

    @functools.cached_property
    def letter_dict(self):
        letters = {}
        c_pitch_class = None
        for i in range(-2, 5):
            if i > 3: # A hack to get F rather than F#, there must be a more elegant way
                i -= 7
            pitch_class = (i * self.fifth) % self.tet
            if c_pitch_class is None:
                c_pitch_class = pitch_class
            pitch_class = (pitch_class - c_pitch_class) % self.tet
            letter = self.alphabet[(3 + i) % len(self.alphabet)]
            letters[letter] = pitch_class
        return letters

    @functools.cached_property
    def spell_dict(self):
        self._init_spell_and_octave_dict()
        return self._spell_dict
    
    @functools.cached_property
    def octave_offsets(self):
        self._init_spell_and_octave_dict()
        return self._octave_offsets

    def _init_spell_and_octave_dict(self):
        self._spell_dict = {}
        self._octave_offsets = {}
        for letter, letter_pc in self.letter_dict.items():
            self._spell_dict[letter_pc] = letter
            self._octave_offsets[letter_pc] = 0
        for j in itertools.count():
            i = j // 2
            flat = j % 2
            n_acc = i // 7 + 1
            letter = self.alphabet[(-1 - (i % 7)) if flat else i % 7]
            letter_pc = self.letter_dict[letter]
            in_place_pc = letter_pc + (-1 if flat else 1) * n_acc * self.m2
            pc = in_place_pc % self.tet
            self._spell_dict[pc] = letter + n_acc * (self.flat_sign if flat else "#")
            self._octave_offsets[pc] = -math.floor(in_place_pc / self.tet)
            if len(self._spell_dict) == self.tet:
                break
