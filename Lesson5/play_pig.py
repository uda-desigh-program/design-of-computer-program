# -----------------
# User Instructions
#
# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored
import random

other = (1, 0)
goal = 50
possible_moves = ['roll', 'hold']

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    p, me, you, pending = state
    return (other[p], you, me+pending, 0)


def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    assert 1 <= d <= 6
    p, me, you, pending = state
    if d == 1:
        return (other[p], you, me+1, 0)
    else:
        return (p, me, you, pending+d)

def dierolls():
    """Generate die rolls."""
    while True:
        yield random.randint(1, 6)

def play_pig(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    (p, me, you, pending) = state = (0, 0, 0, 0)
    while True:
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        elif strategies[p](state) == 'hold':
            (p, me, you, pending) = state = hold(state)
        else: #'roll'
            (p, me, you, pending) = state = roll(state, next(dierolls))

############ STRATEGIES ################

def always_roll(state):
    return 'roll'

def always_hold(state):
    return 'hold'

# just 5/5 random strategy
def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

# hold_at strategies family generator
def hold_at(x):
    """Return a strategy that holds if and only if
    pending >= x or player reaches goal."""
    def strategy(state):
        p, me, you, pending = state
        return 'hold' if (me+pending >= goal or pending >= x) else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy


############ STRATEGIES ################

def test():
    A, B = hold_at(50), clueless
    rolls = iter([6,6,6,6,6,6,6,6,6])
    assert play_pig(A, B, rolls) == A
    return 'test passes'

print test()