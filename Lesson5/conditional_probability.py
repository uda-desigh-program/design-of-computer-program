import itertools
from fractions import Fraction

sex = 'BG'
two_kids = map(''.join, itertools.product(sex, sex))
one_boy = [s for s in two_kids if 'B' in s]

def two_boys(s): return s.count('B') == 2

def condP(predicate, event):
    """Conditional probability: P(predicate(s) | s in event)."""
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

print condP(two_boys, one_boy)

day = 'SMTWtFs'
two_kids_bday = map(''.join, itertools.product(sex, day, sex, day))
one_boy_tday = [s for s in two_kids_bday if 'Bt' in s]
print condP(two_boys, one_boy_tday)