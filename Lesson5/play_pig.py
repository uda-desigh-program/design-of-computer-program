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

#memo codes or use: from Lesson3.memo import memo
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f

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





############### Problem1 ##################
from Lesson2.zebra_puzzle import timedcall
print timedcall(Pwin, State(0,0,0,0))
print len(Pwin.cache)


def Pwin2(state):
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    _, me, you, pending = state
    return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    if me+pending >= goal:
        return 1.0
    elif you >= goal:
        return 0.0
    else:
        Proll = (1-Pwin3(you, me+1,0)+
                 sum(Pwin3(me, you, pending+d) for d in (2,3,4,5,6)))/6
        return Proll if pending == 0 else max(Proll, 1 - Pwin3(you, me+pending, 0))

def test():
    epsilon = 0.0001  # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    print timedcall(Pwin3, *(0, 0, 0))
    print len(Pwin3.cache)
    return 'tests pass'


print test()


"""
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
"""