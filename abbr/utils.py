"""Utilities for abbr
"""
import re
import logging

from nltk.stem import PorterStemmer as Stemmer

LOGGER = logging.getLogger('abbreviations.utils')


def get_res():
    """
    Return regular expression for finding abbreviations and base of
    regex for finding terms.

    Returns
    -------
    re_abbr : _sre.SRE_Pattern
        Regular expression pattern for flagging potential abbreviations in text.

    re_words : _sre.SRE_Pattern
        Regular expression pattern for identifying words preceding parenthetical
        statements in text. Used to replace abbreviations with terms.
    """
    # some of the same regex pieces are used in the make_abbr_regex function
    re_abbr = re.compile('\\s\(([a-zA-Z/]+)s?[\\);]', re.MULTILINE)
    re_words = re.compile("([A-z0-9\-]+('s|s')?)([^A-z0-9\-]*)", re.MULTILINE)

    return re_abbr, re_words


def do_words_match(word1, word2):
    """
    Compare stemmed versions of words.

    Parameters
    -------
    word1 : str
        A word.

    word2 : str
        Another word.

    Returns
    -------
    do_match : bool
        True if the stemmed versions of word1 and word2 are equal.
    """
    try:
        do_match = Stemmer().stem(word1) == Stemmer().stem(word2)
    except:
        do_match = False
    return do_match


def replace(text, abb, fullterm, rep_abbs=True):
    """
    Replace abbreviation abb with term fullterm in text using re.search.

    Parameters
    -------
    text : str
        Text in which to replace abbreviations.

    abb : str
        Abbreviation to expand in text.

    fullterm : str
        Full term associated with abbreviation abb. Will replace instances of
        abb in text.

    rep_abbs : bool, optional
        Whether to replace abbreviation with term (True) or term with
        abbreviation (False).

    Returns
    -------
    text : str
        Text with fullterm replacing every instance of abb.
    """
    _, re_words = get_res()

    if rep_abbs:
        # A more complicated replacement procedure for expanding abbreviations.
        # The goal is to allow for more flexibility in how abbreviations
        # are used in text (e.g., by comparing stemmed versions of abbreviations
        # instead of the canonical version only).
        match = 1
        start_idx = 0
        while match is not None:
            match = re.search(re_words, text[start_idx:])

            if match is not None:
                if do_words_match(match.group(1), abb):
                    w_start = start_idx + match.start()
                    w_end = w_start + len(match.group(1))
                    text = text[:w_start] + fullterm + text[w_end:]
                    temp_idx = w_start + len(fullterm)
                    try:
                        temp_idx2 = re.search(r'\b', text[temp_idx:]).start()
                        start_idx = temp_idx + temp_idx2
                    except:
                        LOGGER.info('Text ends with an abbreviation ({0}). '
                                    'Escaping while loop.'.format(abb))
                        break
                else:
                    start_idx += match.end()
    else:
        # Simple replacement, assuming that the full term is only used in the
        # "canonical" manner. Perhaps we will allow for alternate forms in the
        # future (e.g., using stemming or common rearrangements of words).
        text = re.sub(r'\b{0}\b'.format(fullterm), abb, text)
    return text


def make_abbr_regex(abb_match):
    """
    Each letter in the abbreviation should be in one of the words in the
    full term. Stopwords (e.g., a, of, are) may appear between words in the
    full term.

    Parameters
    -------
    abb_match : _sre.SRE_Match
        Potential match for abbreviation.

    Returns
    -------
    compiled : _sre.SRE_Pattern
        Pattern for finding full term within text.

    """
    # set the abbreviation as nested text string returned by re.finditer
    abb = abb_match.group(1)

    # create an empty regex and list possible separators between words
    regex = ''
    separators = "[A-z/]*('s)?)(\\s((a|of|are|with|the|in|to|)\\s)*|-[A-z/]*)?"

    # iterate through the abbreviation and add each letter to the regex
    for index, letter in enumerate(abb):
        if letter is not '/':
            regex += '(([' + letter.upper() + letter.lower() + ']' + separators + ')'
            if index > 0:
                regex += '?'

    # confirm that a space precedes the matched expression
    # so regex does not match in the middle of a word
    regex = '\s(' + regex + ')'

    # allow for an additional word before the abbreviation is noted in text
    # e.g., substantia nigra compacta (SN)
    regex += '(' + separators

    # confirm that the term is followed by the abbreviation
    regex += '\\(' + abb + '[\\);]'
    compiled = re.compile(regex, re.MULTILINE)
    return compiled
