import re, string, itertools



def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        l = len(word)
        terms = [('%s*%s' % (10**(l-i-1), d))
                 for (i, d) in enumerate(word)]
        return '(' + '+'.join(terms) + ')'
    else:
        return word

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. For example, 'YOU == ME**2' :returns
    (lambda Y,M,E,U,O: (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO'"""
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    firstletters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    if firstletters:
        tests = ' and '.join(L+'!=0' for L in firstletters)
        body = '%s and (%s)' % (tests, body)
    f = 'lambda %s: %s' % (parms, body)
    if verbose: print f
    return eval(f), letters

def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula, True)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str,digits)))
                print formula.translate(table)
        except ArithmeticError:
            pass


#print compile_word('YOU')
#print compile_formula('YOU == ME**2', True)
#python -m cProfile crypt.py
faster_solve('ZOUYU + LIULI == ZHENG')
faster_solve('YU * LILY == FAMILY')