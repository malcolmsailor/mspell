import pytest

from mspell.transpose import transpose_spelling
from mspell.unspeller import Unspeller


@pytest.mark.parametrize("chromatic", list(range(-12, 13)))
@pytest.mark.parametrize("diatonic", list(range(-7, 7)))
def test_transpose(chromatic, diatonic):
    spelled_pitches = ["C", "D", "E", "F", "G", "A", "B"]
    unspeller = Unspeller()
    unspelled = unspeller(spelled_pitches)
    expected_unspelled_transposed = [
        ((p + chromatic) % 12) for p in unspelled  # type:ignore
    ]

    transposed = transpose_spelling(spelled_pitches, chromatic, diatonic)
    unspelled_transposed = unspeller(transposed)

    assert expected_unspelled_transposed == unspelled_transposed

    untransposed = transpose_spelling(transposed, -chromatic, -diatonic)

    assert untransposed == spelled_pitches
