
Fail = []

def successors(x, y, X, Y):
    """Return a dict of {state:action} pairs describing what can be reached from the (x, y) state, and how."""
    assert x<=X and y<=Y
    return {
        ((0, y+x) if y+x<=Y else (x-(Y-y), Y)): 'X->Y',
        ((x+y, 0) if x+y<=X else (X, y-(X-x))): 'X<-Y',
        (X, y): 'fill X', (x, Y): 'fill Y',
        (0, y): 'empty X', (x, 0): 'empty Y'
    }

def pour_problem(X, Y, goal, start=(0, 0)):
    if goal in start:
        return [start]
    explored = set() # set of states we have visited
    frontier = [[start]] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        (x, y) = path[-1] # last state in the path
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

print pour_problem(4, 9, 6)
print pour_problem(7, 9, 8)

"""
for x in range(2,20):
    for y in range(2,20):
        for g in range(2,max(x, y)):
            if not pour_problem(x, y, g):
                print x, y, g
"""