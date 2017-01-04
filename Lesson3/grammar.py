import re

def grammar(description, whitespace=r'\s*'):
    """"Convert a description to a grammar."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "Like string.split applied to text, but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

G = grammar(r"""
Exp     =>  Term [+-] Exp | Term
Term    =>  Factor [*/] Term | Factor
Factor  =>  Funcall | Var | Num | [(] Exp [)]
Funcall =>  Var [(] Exps [)]
Exps    =>  Exp [,] Exps | Exp
Var     =>  [a-zA-Z_]\w*
Num     =>  [-+]?[0-9]+([.][0-9]*)?
""")

from memo import memo

def parse(start_symbol, text, grammar):
    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar: # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree,rem
            return Fail
        else: #Terminal: macth characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

print G['Exps']
a, b = parse('Funcall', 'abs(-1)', G)
print 'A: ', a
print 'B: ', b

# try this grammer:
# https://www.w3.org/Addressing/URL/5_BNF.html