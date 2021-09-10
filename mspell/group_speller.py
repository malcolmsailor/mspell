from typing import Optional, Sequence
import numpy as np

import math

from . import utils

from .utils import get_accidental


class GroupSpeller:
    """Finds the 'best' spelling for lists of pitch-classes.

    'Best' is defined as having both
      - the shortest span on the line of fifths, and
      - the least absolute summed distance from 'D' (the central pitch of the
        white-key diatonic)

    The Pythagorean approach to spelling taken only works if the greatest common
    denominator of the (approximation to the just) fifth and the temperament
    cardinality is 1. In other words, a cycle of perfect fifths must reach every
    pitch-class. If this is not true, raises a ValueError.

    Keyword args:
        tet: sets temperament.

    Methods:
        __call__: takes a sequence of ints, returns an np array of strings

    Raises:
        ValueError if gcd(tet, fifth) is not 1.
    """

    # keys: temperament cardinalities
    # values: tuples of form (fifth, zero_pc)
    tet_dict = {
        12: (7, 2),
        19: (11, 3),
        31: (18, 5),
    }

    def __init__(self, tet: int = 12):
        self.tet = tet
        if tet in self.tet_dict:
            self.fifth, self.zero_pc = self.tet_dict[tet]
        else:
            self.fifth = utils.approximate_just_interval(3 / 2, tet)
            if math.gcd(tet, self.fifth) != 1:
                raise ValueError
            self.zero_pc = 2 * self.fifth % self.tet
        self._shell_dict = self.build_fifth_class_spelling_dict()
        self._kern_dict = self.build_fifth_class_spelling_dict(
            letter_format="kern"
        )

    @staticmethod
    def build_fifth_class_spelling_dict(
        bounds: tuple[int, int] = (-28, 28),
        forward: bool = True,
        letter_format: str = "shell",
    ) -> dict:
        flat_sign = "b" if letter_format == "shell" else "-"
        alphabet = "DAEBFCG" if letter_format == "shell" else "daebfcg"
        len_alphabet = 7
        out = {}
        for fc in range(bounds[0], bounds[1] + 1):
            letter = alphabet[fc % len_alphabet]
            accidental = get_accidental(
                math.floor((fc + 3) / len_alphabet), flat_sign=flat_sign
            )
            if forward:
                out[fc] = letter + accidental
            else:
                out[letter + accidental] = fc
        return out

    def _pc_to_fc(self, pc: int) -> int:
        # return (pc - self.ref_pc) * self.fifth % self.tet - self.half_tet
        return (pc - self.zero_pc) * self.fifth % self.tet

    def __call__(
        self, pcs: Sequence[int], letter_format: str = "shell"
    ) -> list[str]:
        """
        Args:
            pcs: sequence of ints.

        Keyword args:
            letter_format: either "shell" (C#, Bb, ...) or "kern" (c#, b-, ...)
        """
        if len(pcs) == 0:
            return []
        unique_pcs, inv_indices = np.unique(pcs, return_inverse=True)
        fcs = self._pc_to_fc(unique_pcs)
        indices = np.argsort(fcs)
        lower_bound = None
        span = fcs[indices[-1]] - fcs[indices[0]]
        if span > 6:
            for i, j in zip(indices, indices[1:]):
                newspan = (fcs[i] + self.tet) - fcs[j]
                if newspan < span:
                    lower_bound = fcs[j]
                    span = newspan
            if lower_bound is not None:
                fcs = np.array(
                    [fc + self.tet if fc < lower_bound else fc for fc in fcs]
                )
        fcs_sum = fcs.sum()
        while True:
            flat_fcs = fcs - self.tet
            flat_sum = abs(flat_fcs.sum())
            if flat_sum < fcs_sum:
                fcs = flat_fcs
                fcs_sum = flat_sum
            else:
                break
        if letter_format == "shell":
            spellings = [self._shell_dict[fc] for fc in fcs]
        else:
            spellings = [self._kern_dict[fc] for fc in fcs]
        return list(np.array(spellings)[inv_indices])

    def pitches(
        self,
        pitches: Sequence[Optional[int]],
        letter_format: str = "shell",
        rests: Optional[str] = None,
    ) -> list[str]:
        """Takes a sequence of ints, returns a list array of spelled strings.

        Args:
            pitches: sequence of ints (and possibly NoneType, if rests is
                passed).

        Keyword args:
            letter_format: either "shell" (C#4, Bb2, ...)
                or "kern" (cc#, B-, ...)
            rests: if passed, then any items in `pitches` with the value of
                `None` will be replaced with this value.
        """

        def _kern_octave(pitch, letter):
            octave = pitch // self.tet - 5
            if octave >= 0:
                return letter * (octave + 1)
            return letter.upper() * (-octave)

        if rests is not None:
            pitches = list(pitches)
            rest_indices = [
                i for (i, pitch) in enumerate(pitches) if pitch is None
            ]
            for i in reversed(rest_indices):
                pitches.pop(i)

        pcs = self(pitches, letter_format=letter_format)

        # The next three lines (and the subtraction of alterations below) ensure
        # that Cb or B# (or even Dbbb, etc.) appear in the correct octave. It
        # feels a little hacky, but it works.
        sharp_sign = "#"
        flat_sign = "b" if letter_format == "shell" else "-"
        alterations = [
            0 + pc.count(sharp_sign) - pc.count(flat_sign) for pc in pcs
        ]

        if letter_format == "shell":
            out = [
                pc + str((pitch - alteration) // self.tet - 1)
                for (pitch, pc, alteration) in zip(pitches, pcs, alterations)
            ]
        else:
            out = [
                _kern_octave(pitch - alteration, pc[0]) + pc[1:]
                for (pitch, pc, alteration) in zip(pitches, pcs, alterations)
            ]
        if rests is not None:
            for i in rest_indices:
                out.insert(i, rests)
        return out
