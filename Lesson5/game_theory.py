import math

million = 1000000

def Q(state, action, U):
    """The expected value of taking action in state, according to utility U."""
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        return U(state+3*million)*.5 + U(state)*.5

def actions(state): return ['hold', 'gamble']

def identity(x): return x

U = math.log10

def best_action(state, actions, Q, U):
    """Return the optimal action for a state, given U."""
    def EU(action): return Q(state, action, U) #Expected Utility
    return max(actions(state), key=EU)

print best_action(100, actions, Q, identity)

print best_action(100, actions, Q, math.log10)

print best_action(10000000, actions, Q, math.log10)