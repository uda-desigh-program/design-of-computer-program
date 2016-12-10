def sq(x): print 'sq called', x; return x*x

def generator_test():
    g = (sq(x) for x in range(6) if x % 2 == 0)
    next(g)
    g.next()
    next(g)
    g.next()

#generator_test()