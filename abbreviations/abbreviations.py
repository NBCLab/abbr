import re
from glob import glob
import pandas as pd
from os.path import join
from collections import Counter
from .utils import make_abbr_regex, get_res, replace


def findall(text):
    """
    Find, but don't expand, abbreviations in the text. Returns a
    dictionary of (abbreviation: full term). Abbreviations with no found
    term will have None value and will not be expanded in
    expand_abbreviations.

    Parameters
    ----------
    text : str
        Text to search for abbreviations.

    Returns
    -------
    abbrevs: dict
        Dictionary of (abbreviation: full term) items. Abbreviations with no
        associated term will be returned with None value. Associated function
        `expand_abbreviations` will ignore abbreviations with no full term.

    Examples
    ----------
    >>> text = 'This is a test string (TS). I hope it is informative (inf).'
    >>> abbrevs = findall(text)
    >>> print(abbrevs)
    {'inf': 'informative', 'TS': 'test string'}
    """
    re_abbr, _ = get_res()

    abbrevs = {}
    f = re.finditer(re_abbr, text)
    for match in f:
        if match is not None:
            abb = str(match.group(1))

            # Very long abbreviations will break regex.
            if len(abb) < 17:
                abR = make_abbr_regex(match)

                fullterm = re.search(abR, text)

                if fullterm is not None:
                    abbrevs[abb] = str(fullterm.group(1)[:-1])
                else:
                    abbrevs[abb] = None
    return abbrevs


def expandall(text):
    """
    Search for abbreviations in text using re_abbr (defined in utils.get_res).
    For each abbreviation, find likely full term. Replace each instance of the
    abbreviation in the text with the full term.

    Parameters
    ----------
    text : str
        Text to search for abbreviations.

    Returns
    -------
    text: str
        Text with expanded abbreviations.

    Examples
    ----------
    >>> text = 'This is a test string (TS). I hope it is informative (inf).'
    >>> expanded = expandall(text)
    >>> print(expanded)
    This is a test string (test string). I hope it is informative (informative).
    """
    re_abbr, _ = get_res()

    f = re.finditer(re_abbr, text)
    for match in f:
        if match is not None:
            abR = make_abbr_regex(match)
            abb = match.group(1)
            fullterm = re.search(abR, text)

            if fullterm is not None:
                text = replace(text, abb, fullterm.group(1)[:-1])
            else:
                print('Empty: {0}'.format(abb))
    return text


def find_corpus(folder, clean=True):
    """
    Find all abbreviations in a corpus (folder of text files). Returns a
    dataframe containing the abbreviations, terms associated with each unique
    abbreviation, and count for each term.

    Parameters
    ----------
    folder : str
        Folder containing text files from which to build abbreviations
        dictionary.

    clean : bool
        Determines whether or not to process text strings within files using
        clean_str. Default = True

    Returns
    -------
    df : pandas DataFrame
        DataFrame with three columns: abbreviation, term, and count.
        abbreviation:   Abbreviations found in the corpus. Not necessarily
                        unique. Different files may have the same abbreviation
                        defined differently.
        term:           Term associated with each abbreviation. Not necessarily
                        unique. Different files may have the same term
                        abbreviated differently.
        count:          The number of documents in which a given
                        (abbreviation, term) appears. Can be used to evaluate
                        prevalence of pairs within the corpus.
    """
    corpus_abbs = {}

    files = glob(join(folder, '*.txt'))
    for f in files:
        with open(f, 'rb') as fo:
            text = fo.read()

        if clean:
            text = clean_str(text)
        abbs = findall(text)
        abbs = {k: [v] for (k, v) in abbs.items() if v is not None}
        keys = set(corpus_abbs).union(abbs)
        no = []
        corpus_abbs = dict((k, corpus_abbs.get(k, no) + abbs.get(k, no)) for k in keys)

    # Count number of documents in which a given (abb, term) pair occurs.
    corpus_abbs = {k: Counter(v) for (k, v) in corpus_abbs.items()}

    # Convert dict of Counters to DataFrame.
    results = []
    for abb in corpus_abbs.keys():
        for term in corpus_abbs[abb].keys():
            count = corpus_abbs[abb][term]
            results.append([abb, term, count])
    df = pd.DataFrame(data=results, columns=['abbreviation', 'term', 'count'])
    return df


def clean_str(text):
    """
    Apply some standard text cleaning with regex.
        1. Remove unicode characters.
        2. Combine multiline hyphenated words.
        3. Remove newlines and extra spaces.

    Parameters
    ----------
    text : str
        Text to clean.

    Returns
    ----------
    text : str
        Cleaned text.

    Examples
    ----------
    >>> text = 'I am  a \nbad\r\n\tstr-\ning.'
    >>> print(text)
    I am  a
    bad
        str-
    ing.
    >>> text = clean_str(text)
    >>> print(text)
    I am a bad string.
    """
    # Remove unicode characters.
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Combine multiline hyphenated words.
    text = re.sub('-[\s]*[\r\n\t]+', '', text, flags=re.MULTILINE)

    # Remove newlines and extra spaces.
    text = re.sub('[\r\n\t]+', ' ', text, flags=re.MULTILINE)
    text = re.sub('[\s]+', ' ', text, flags=re.MULTILINE)
    return text
