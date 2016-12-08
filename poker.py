def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return max(hands, key=hand_rank3)
    #return max(hands, key=hand_rank) or hand_rank2

def allmax(iterable, key=None):
    return [x for x in iterable if key(x) == key(max(iterable, key=key))]
    # # This solution is given by teacher, all passed the test
    # for x in iterable:
    #     xval = key(x)
    #     if not res or xval > maxval:
    #         res, maxval = [x], xval
    #     elif xval == maxval:
    #         res.append(x)
    # return res


def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first"
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    if ranks == [14, 5, 4, 3, 2]:
        return True
    else:
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

def two_pair(ranks):
    res = []
    for r in ranks:
        if 2 == ranks.count(r) and 0 ==res.count(r):
            res.append(r)
    if len(res) == 2:
        return tuple(res)
    else:
        return None

# this is the solution teacher given, both passed
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

def hand_rank2(hand):
    "Return a value indicating how high the hand ranks"
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    is_straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    is_flush = len(set(s for r,s in hand)) == 1
    return (9 if (5,) == counts else
            8 if is_straight and is_flush else
            7 if (4,1) == counts else
            6 if (3,2) == counts else
            5 if is_flush else
            4 if is_straight else
            3 if (3,1,1) == counts else
            2 if (2,2,1) == counts else
            1 if (2,1,1,1) == counts else
            0), ranks

def group(ranks):
    "Return a list of [(count, x), ...], highest count first, then highest x first"
    groups = [(ranks.count(x), x) for x in set(ranks)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    return zip(*pairs)

def hand_rank3(hand):
    "Return a value indicating how high the hand ranks"
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    count_rankings = {(5,):10, (4,1):7, (3,2):6, (3,1,1):3, (2,2,1):2, (2,1,1,1):1, (1,1,1,1,1):0}
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    is_straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    is_flush = len(set(s for r,s in hand)) == 1
    return max(count_rankings[counts], 4*is_straight+5*is_flush), ranks

def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5D 5H 9H 9C 3S".split() # Two Pair
    s5 = "5D 4C 3H 2D AC".split()
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)

    assert group([5,5,7,7,7]) == [(3,7),(2,5)]
    assert group([5, 10, 5, 14, 14]) == [(2, 14), (2, 5), (1, 10)]
    assert group([5, 2, 3, 14, 4]) == [(1, 14), (1, 5), (1, 4), (1, 3), (1, 2)]

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert kind(3, card_ranks(fh)) == 10


    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)
    assert two_pair(card_ranks(sf)) == None
    assert two_pair([5, 5, 4, 3, 3]) == (5,3)

    assert straight(card_ranks(sf)) == True
    assert straight([6, 5, 4, 3, 2]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert straight([14, 13, 12, 11, 10]) == True
    assert straight([14, 5, 4, 3, 2]) == True
    assert straight(card_ranks(s5)) == True

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

    assert allmax([sf, sf], hand_rank3) == [sf, sf]
    assert allmax(2*[sf]+3*[fk]+4*[fh], hand_rank3) == 2*[sf]

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7, [10, 10, 10, 7, 7])

    assert hand_rank2(sf) == (8, (10, 9, 8, 7, 6))
    assert hand_rank2(fk) == (7, (9, 7))
    assert hand_rank2(fh) == (6, (10, 7))

    assert hand_rank3(sf) == (9, (10, 9, 8, 7, 6))
    assert hand_rank3(fk) == (7, (9, 7))
    assert hand_rank3(fh) == (6, (10, 7))

    return "test pass"

print test()
#print timeit.timeit('test', 'from poker import test',number=10000000)
