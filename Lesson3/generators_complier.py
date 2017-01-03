
def lit(s):
    set_s = set([s])
    return lambda Ns: set_s if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx=1)  # Tricky
def oneof(chars):
    set_c = set(chars)
    return lambda Ns: set_c if 1 in Ns else null
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)

def genseq(x, y, Ns, startx=0):
    if not Ns: return null
    xmatches = x(set(range(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m>=0)
    ymatches = y(Ns_y)
    return set(m1+m2
               for m1 in xmatches for m2 in ymatches
               if len(m1+m2) in Ns)


dot = oneof('?')  # You could expand the alphabet to more chars.
epsilon = lit('')  # The pattern that matches the empty string.

null = frozenset([])

def test():
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4])) == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null

    m = plus(lit('hi'))
    print m(set([1,2,3,4,5,6,7,8,9]))

    #test gen
    def N(hi): return set(range(hi+1))
    a,b,c, = map(lit, 'abc')
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert seq(star(a), seq(star(b), star(c)))(set([4])) == set(['aaaa', 'bccc', 'abbc', 'abbb', 'abcc', 'aacc', 'bbcc', 'aabc', 'bbbb', 'bbbc', 'accc', 'cccc', 'aaac', 'aaab', 'aabb'])
    assert seq(plus(a), seq(plus(b), plus(c)))(set([5])) == set(['aaabc', 'abbbc', 'abbcc', 'aabcc', 'aabbc', 'abccc'])
    assert seq(oneof('bcfhrsm'), lit('at'))(N(3)) == set(['bat', 'mat', 'fat', 'cat', 'rat', 'hat', 'sat'])
    assert seq(star(alt(a,b)), opt(c))(set([3])) == set(['aba', 'abb', 'abc', 'aaa', 'aac', 'aab', 'bbc', 'bbb', 'bba', 'bab', 'bac', 'baa'])
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()

    return 'tests pass'


print test()