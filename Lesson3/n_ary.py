from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

"""
# also work
def decorator(d):
    return lambda fn: update_wrapper(d(fn), fn)
decorator = decorator(decorator)
"""

@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

@n_ary
def add(x, y):
    return x + y

@n_ary
def mul(x, y):
    return x*y

#print add(1, 2)
print add(1)
print add(1,2)
print add(1,2,3)
print add(1,2,3,4)


print mul(1)
print mul(1,2)
print mul(1,2,3)
print mul(1,2,3,4)

print help(add)