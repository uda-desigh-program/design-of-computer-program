# -----------------
# User Instructions
#
# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored
import random
from collections import namedtuple

other = (1, 0)
goal = 40
possible_moves = ['roll', 'hold']
State = namedtuple('State', 'p me you pending')

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    return State(other[state.p], state.you, state.me+state.pending, 0)


def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    assert 1 <= d <= 6
    if d == 1:
        return State(other[state.p], state.you, state.me+1, 0)
    else:
        return State(state.p, state.me, state.you, state.pending+d)

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
    state = State(0, 0, 0, 0)
    while True:
        if state.me >= goal:
            return strategies[state.p]
        elif state.you >= goal:
            return strategies[other[state.p]]
        else:
            action = strategies[state.p](state)
            if action == 'hold':
                state = hold(state)
            elif action == 'roll':
                state = roll(state, next(dierolls))
            else: # illegal action
                return strategies[other[state.p]]


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


############ OPTIMAL PIG ################

def Q_pig(state, action, U_pig):
    """The expected value of choosing action in state."""
    if action == 'hold':
        return 1 - U_pig(hold(state))
    elif action == 'roll':
        return (1 - U_pig(roll(state, 1)) + sum(U_pig(roll(state, d)) for d in (2,3,4,5,6))) / 6.0
    raise ValueError

def pig_actions(state):
    """the legal actions from a state"""
    return ['roll', 'hold'] if state.pending else ['roll']

from Lesson3.memo import memo

@memo
def Pwin(state):
    """The utility of a state; here just the probability that an opltimal player
     whose turn it is to move can  win from current state."""
    if state.me+state.pending >= goal:
        return 1.0
    elif state.you >= goal:
        return 0.0
    else:
        return max(Q_pig(state, action, Pwin)
                   for action in pig_actions(state))


def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)

#the max win probability Strategy
def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    s = State(*state)
    return best_action(s, pig_actions, Q_pig, Pwin)

######### MAX DIFFERENTIAL PIG #############
@memo
def win_diff(state):
    "The utility of a state: here the winning differential (pos or neg)."
    if state.me + state.pending >= goal or state.you >= goal:
        return (state.me + state.pending - state.you)
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in pig_actions(state))

#the max differential Strategy
def max_diffs(state):
    """A strategy that maximizes the expected difference between my final score
    and my opponent's."""
    s = State(*state)
    return best_action(s, pig_actions, Q_pig, win_diff)



def test():
    assert(max_wins((1, 5, 34, 4)))   == "roll"
    assert(max_wins((1, 18, 27, 8)))  == "roll"
    assert(max_wins((0, 23, 8, 8)))   == "roll"
    assert(max_wins((0, 31, 22, 9)))  == "hold"
    assert(max_wins((1, 11, 13, 21))) == "roll"
    assert(max_wins((1, 33, 16, 6)))  == "roll"
    assert(max_wins((1, 12, 17, 27))) == "roll"
    assert(max_wins((1, 9, 32, 5)))   == "roll"
    assert(max_wins((0, 28, 27, 5)))  == "roll"
    assert(max_wins((1, 7, 26, 34)))  == "hold"
    assert(max_wins((1, 20, 29, 17))) == "roll"
    assert(max_wins((0, 34, 23, 7)))  == "hold"
    assert(max_wins((0, 30, 23, 11))) == "hold"
    assert(max_wins((0, 22, 36, 6)))  == "roll"
    assert(max_wins((0, 21, 38, 12))) == "roll"
    assert(max_wins((0, 1, 13, 21)))  == "roll"
    assert(max_wins((0, 11, 25, 14))) == "roll"
    assert(max_wins((0, 22, 4, 7)))   == "roll"
    assert(max_wins((1, 28, 3, 2)))   == "roll"
    assert(max_wins((0, 11, 0, 24)))  == "roll"

    # The first three test cases are examples where max_wins and
    # max_diffs return the same action.
    assert (max_diffs((1, 26, 21, 15))) == "hold"
    assert (max_diffs((1, 23, 36, 7))) == "roll"
    assert (max_diffs((0, 29, 4, 3))) == "roll"
    # The remaining test cases are examples where max_wins and
    # max_diffs return different actions.
    assert (max_diffs((0, 36, 32, 5))) == "roll"
    assert (max_diffs((1, 37, 16, 3))) == "roll"
    assert (max_diffs((1, 33, 39, 7))) == "roll"
    assert (max_diffs((0, 7, 9, 18))) == "hold"
    assert (max_diffs((1, 0, 35, 35))) == "hold"
    assert (max_diffs((0, 36, 7, 4))) == "roll"
    assert (max_diffs((1, 5, 12, 21))) == "hold"
    assert (max_diffs((0, 3, 13, 27))) == "hold"
    assert (max_diffs((0, 0, 39, 37))) == "hold"

    return 'tests pass'

print test()