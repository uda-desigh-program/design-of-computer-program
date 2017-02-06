

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]


def readwordlist(filename):
    """Read the words from a file and return a set of the words
    and a set of the prefixes."""
    file = open(filename)  # opens file
    text = file.read()  # gets file into string
    wordset = set(text.upper().splitlines())
    prefixset = set(p for word in wordset for p in prefixes(word))
    """
    for word in text.split('\n'):
        wordset.add(word)
        for prefix in prefixes(word):
            prefixset.add(prefix)
    """
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')

def find_words(letters, pre='', results=None):
    if results is None: results = set()
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), pre+L, results)
    return results

def m():
    assert len(WORDS) == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES

    print find_words('AAB')

    return 'tests pass'


print m()