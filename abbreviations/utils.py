import re
from nltk.stem import PorterStemmer as Stemmer


def get_res():
    """ Return regular expression for finding abbreviations and base of
    regex for finding terms.
    """
    # some of the same regex pieces are used in the make_abbr_regex function
    re_abbr = re.compile('\\(([a-zA-Z]+)s?[\\);]', re.MULTILINE)
    re_words = re.compile("([A-z0-9\-]+('s|s')?)([^A-z0-9\-]*)", re.MULTILINE)

    return re_abbr, re_words


def do_words_match(A, B):
    """ Compare stemmed versions of words.
    """
    return Stemmer().stem(A) == Stemmer().stem(B)


def replace(text, A, B):
    """ Replace abb A with term B in text.
    """
    _, re_words = get_res()

    match = -1
    start_idx = 0
    while match is not None or match == -1:
        match = re.search(re_words, text[start_idx:])
        if match is not None:
            if do_words_match(match.group(1), A):
                w_start = start_idx + match.start()
                text = text[:w_start] + B + text[w_start+len(match.group(1)):]

            start_idx += match.end()
    return text


def make_abbr_regex(abb_match):
    """
    Each letter in the abbreviation should start one of the words in the
    full term. Stopwords (e.g., a, of, are) may appear between words in the
    full term.
    """
    abb = abb_match.group(1)
    regex = ''
    separators = "[A-z]*('s)?)(\\s((a|of|are|with|the|in|to)\\s)?|-[A-z]*)?"
    for index, c in enumerate(abb):
        regex += '((['+c.upper() + c.lower()+']'+separators+')'
        if index > 0:
            regex+='?'
    regex = '\s('+regex+')'
    regex += '\\('+abb_match.group()[1:-1]+'[\\);]'
    return re.compile(regex, re.MULTILINE)
