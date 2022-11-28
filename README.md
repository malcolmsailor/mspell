A library for spelling and unspelling musical pitches.

"Spelling" a pitch is going from an integer to a letter (and, optionally, an accidental and octave number). "Unspelling" a pitch is doing the reverse.

Provides the following three classes, instances of each of which are callable:

```
Speller
Unspeller
Groupspeller
```

# Requirements

numpy

If Pandas or Pytorch are installed, supports spelling Series or Tensors respectively.

# Example usage

```
>>> import mspell
>>> speller = mspell.Speller()
>>> speller(6)
'F#'
>>> speller([3,6,10])
['Eb', 'F#', 'Bb']
>>> groupspeller = mspell.GroupSpeller()
>>> groupspeller([3,6,10])
['Eb', 'Gb', 'Bb']
>>> unspeller = mspell.Unspeller(tet=31)
>>> unspeller([['Eb', 'Gb', 'Bb'], ['Eb', 'F#', 'Bb']])
[[8, 16, 26], [8, 15, 26]]
```
