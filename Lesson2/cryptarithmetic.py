# -------------
# User Instructions
#
# Write a function, solve(formula) that solves cryptarithmetic puzzles.
# The input should be a formula like 'ODD + ODD == EVEN', and the
# output should be a string with the digits filled in, or None if the
# problem is not solvable.
from __future__ import division
import string, re, itertools


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f
    return None

def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)

def valid(f):
    "Formula f is valid iff it has no numbers with leading zero and evals true."
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ZeroDivisionError: #except ArithmeticError:
        return False

examples = """TWO+TWO==FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X/X == X
A**N+B**N== C**N and N>1
ATOM**0.5 == A+TO+M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3+RM**3 == N**3+RX**3
sum(range(AA)) == BB
sum(range(POP))== BOBO
ODD+ODD==EVEN
PLUTO not in set([PLANETS])""".splitlines()
import time
def test():
    t0 = time.clock()
    for ex in examples:
        print '\n', ex
        print solve(ex)
    print time.clock()-t0

test()
"""
print solve('ODD + ODD == EVEN')
print solve('ONE + ONE == TWO')
print solve('SEND + MORE == MONEY')
print solve('THREE+ THREE+ ONE ==SEVEN')
print solve('USA+USSR==PEACE')
#print solve('ZHENG + LIULI == ZOUYU')"""