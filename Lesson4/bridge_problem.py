# -----------------
# User Instructions
#
# Modify the bridge_problem(here) function so that it
# tests for goal later: after pulling a state off the
# frontier, not when we are about to put it on the
# frontier.
import doctest

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and
    '<-' for there to here."""
    here, there, t = state
    if 'light' in here:
        return dict(
            ((here - frozenset([a, b, 'light']),
              there | frozenset([a, b, 'light'])),
             (a, b, '->'))
            for a in here if a is not 'light'
            for b in here if b is not 'light'
        )

    else: #light in there
        return dict(
            ((here | frozenset([a, b, 'light']),
             there - frozenset([a, b, 'light']), t+max(a,b)),
             (a, b, '<-'))
            for a in there if a is not 'light'
            for b in there if b is not 'light'
        )

def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here, frozenset(), 0)] ]
    while frontier:
        path = frontier.pop(0)
        if not path[-1][0] or path[-1][0] == set(['light']):
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []

def elapsed_time(path):
    return path[-1][2]

def path_states(path):
    "Return a list of states in this path."
    return path[::2]

def path_actions(path):
    "Return a list of states in this path."
    return path[1::2]

class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

"""

#print doctest.testmod()


def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a
    (here, there) tuple, where here and there are frozensets
    of people (indicated by their travel times) and/or the light."""
    here, there = state
    if 'light' in here:
        return dict(
            ((here - frozenset([a, b, 'light']),
              there | frozenset([a, b, 'light'])),
             (a, b, '->'))
            for a in here if a is not 'light'
            for b in here if b is not 'light'
        )

    else:  # light in there
        return dict(
            ((here | frozenset([a, b, 'light']),
              there - frozenset([a, b, 'light'])),
             (a, b, '<-'))
            for a in there if a is not 'light'
            for b in there if b is not 'light'
        )

def bridge_problem2(here):
    #TODO more efficient solution only take (here, there) as the state
    pass

def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    # path = (state, (action, total_cost), state, ... )
    if len(path) < 3:
        return 0
    else:
        return path[-2][-1]

def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are
    # times; arrow is a string.
    a, b, arrow = action
    return max(a, b)

