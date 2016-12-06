def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return max(hands, key=hand_rank)

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first"
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks) == min(ranks) + 4) and len(set(ranks)) == 5

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if n == ranks.count(r):
            return r
    return None

# why this failed?
def two_pair(rank):
    res = []
    for r in rank:
        if 2 == rank.count(r) and 0 ==res.count(r):
            res.append(r)

    if len(res) == 2:
        return tuple(res)
    else:
        return None

# this is the solution teacher given
# def two_pair(rank):
#     """If there are two pair, return the two ranks as a
#     tuple: (highest, lowest); otherwise return None."""
#     hp = kind(2, rank)
#     lp = kind(2, list(reversed(rank)))
#     if hp and hp != lp:
#         return (hp, lp)
#     else:
#         return None

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand): # straight flush
        return (8, max(ranks))
    elif kind(4, ranks): # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):  # full house
        return (6, kind(3, ranks), kind(2, ranks), ranks)
    elif flush(hand):  # flush
        return (5, ranks)
    elif straight(ranks):  # straight
        return (4, max(ranks))
    elif kind(3, ranks):  # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):  # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):  # kind
        return (1, kind(2, ranks), ranks)
    else:  # high card
        return  (0, ranks)

def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5D 5H 9H 9C 3S".split() # Two Pair
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert kind(3, card_ranks(fh)) == 10


    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)
    assert two_pair(card_ranks(sf)) == None
    print two_pair([9,8,6,4,2])
    #assert two_pair([3,3,4,5,5]) == (5,3)

    tp2 = "TD 9H TH 9C 3S".split()  # Two Pair2
    tpranks2 = card_ranks(tp2)
    print two_pair(tpranks2)

    assert straight(card_ranks(sf)) == True
    assert straight([6, 5, 4, 3, 2]) == True
    assert straight([9, 8, 8, 6, 5]) == False

    assert flush(sf) == True
    assert flush(fk) == False

    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([sf, sf]) == sf
    assert poker([sf]) == sf
    assert poker([sf]+99*[fh]) == sf

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7, [10, 10, 10, 7, 7])

    return "test pass"

print test()