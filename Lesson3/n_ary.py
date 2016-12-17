def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

def add(x, y):
    return x + y

#print add(1, 2)
t = n_ary(add)
#print t(1)
#print t(1,2)
print t(1,2,3)