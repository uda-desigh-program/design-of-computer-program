
def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    if(M1 < 0 or C1 < 0 or M2 < 0 or C2 < 0): return {}
    if(0 < M1 < C1 or 0 < M2 < C2): return {}
    elif B1 == 1:
        return {
            (M1, C1-1, 0, M2, C2+1, 1): 'C->',
            (M1-1, C1, 0, M2+1, C2, 1): 'M->',
            (M1-2, C1, 0, M2+2, C2, 1): 'MM->',
            (M1-1, C1-1, 0, M2+1, C2+1, 1): 'MC->',
            (M1, C1-2, 0, M2, C2+2, 1): 'CC->'
        }
    else: # B2 == 1
        return {
            (M1, C1+1, 1, M2, C2-1, 0): '<-C',
            (M1+1, C1, 1, M2-1, C2, 0): '<-M',
            (M1+2, C1, 1, M2-2, C2, 0): '<-MM',
            (M1, C1+2, 1, M2, C2-2, 0): '<-CC',
            (M1+1, C1+1, 1, M2-1, C2-1, 0): '<-MC'
        }

def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    """Solve the missionaries and cannibals problem.
    State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) sides.
    Find a path that goes from the initial state to the goal state (which, if
    not specified, is the state with no people or boats on the start side."""
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    if start == goal:
        return [start]
    explored = set()  # set of states we have visited
    frontier = [[start]]  # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

print mc_problem()