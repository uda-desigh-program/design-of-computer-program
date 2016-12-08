# -----------
# User Instructions
#
# Write a function, deal(numhands, n=5, deck), that
# deals numhands hands with n cards each.
#

import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. If you are unfamiliar
# with this notation, check out Andy's supplemental video
# on list comprehensions (you can find the link in the
# Instructor Comments box below).

from poker import hand_rank

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    return [deck[i*n:i*n+n] for i in range(numhands)]
    #print [[cards for cards in mydeck[i * 5:j + 5]] for i in range(2) for j in range(5)]

def hands_percentages(n=700*1000):
    counts = 9*[0]
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for t in counts:
        print "%6.3f %%" % (100.0*t/n)


print deal(8, n = 2,deck=mydeck)
hands_percentages()
# https://en.wikipedia.org/wiki/Poker_probability
