# -*- coding: utf-8 -*-
"""
Created on Feb 4, 2016
Identify and expand abbreviations in text.

@author: Jason Hays (jhays006)
"""

import re
from nltk.stem import PorterStemmer as Stemmer


def findall(text):
    """ Find, but don't expand, abbreviations in the text. Returns a
    dictionary of (abbreviation: full term). Abbreviations with no found
    term will have None value and will not be expanded in
    expand_abbreviations.
    """
    re_abbr, _ = get_res()
    
    abb_dict = {}
    f = re.finditer(re_abbr, text)
    for match in f:
        if match is not None:
            abR = __make_abbr_regex(match)
            abb = str(match.group(1))
            fullterm = re.search(abR, text)
            
            if fullterm is not None:
                abb_dict[abb] = str(fullterm.group(1)[:-1])
            else:
                abb_dict[abb] = None
    return abb_dict


def expandall(text):
    """ Search for abbreviations in text using __re_abbr.
    For each abbreviation, find candidate terms and
    """
    re_abbr, _ = get_res()
    
    f = re.finditer(re_abbr, text)
    for match in f:
        if match is not None:
            abR = __make_abbr_regex(match)
            abb = match.group(1)
            fullterm = re.search(abR, text)
            
            if fullterm is not None:
                text = __replace(text, abb, fullterm.group(1)[:-1])
            else:
                print('Empty: {0}'.format(abb))
    return text


def get_res():
    """ Return regular expression for finding abbreviations and base of
    regex for finding terms.
    """
    # some of the same regex pieces are used in the make_abbr_regex function
    re_abbr = re.compile('\\(([a-zA-Z]+)s?[\\);]', re.MULTILINE)
    re_words = re.compile("([A-z0-9\-]+('s|s')?)([^A-z0-9\-]*)", re.MULTILINE)
    
    return re_abbr, re_words


def __do_words_match(A, B):
    """ Compare stemmed versions of words.
    """
    return Stemmer().stem(A) == Stemmer().stem(B)


def __replace(text, A, B):
    """ Replace abb A with term B in text.
    """
    _, re_words = get_res()
    
    match = -1
    startIndex = 0
    while match is not None or match == -1:
        match = re.search(re_words, text[startIndex:])
        if match is not None:
            if __do_words_match(match.group(1), A):
                wordStart = startIndex + match.start()
                text = text[:wordStart] + B + text[wordStart+len(match.group(1)):]

            startIndex += match.end()
    return text


def __make_abbr_regex(abbMatch):
    """
    Each letter in the abbreviation should start one of the words in the
    full term. Stopwords (e.g., a, of, are) may appear between words in the
    full term.
    """
    abb = abbMatch.group(1)
    regex = ''
    separators = "[A-z]*('s)?)(\\s((a|of|are|with|the|in|to)\\s)?|-[A-z]*)?"
    for index, c in enumerate(abb):
        regex += '((['+c.upper() + c.lower()+']'+separators+')'
        if index > 0:
            regex+='?'
    regex = '\s('+regex+')'
    regex += '\\('+abbMatch.group()[1:-1]+'[\\);]'
    return re.compile(regex, re.MULTILINE)
