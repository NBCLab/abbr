# -*- coding: utf-8 -*-
"""
Created on Feb 4, 2016
Identify and expand abbreviations in text.

@author: Jason Hays (jhays006)
"""

import re
from .utils import make_abbr_regex, get_res, replace


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
            abR = make_abbr_regex(match)
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
            abR = make_abbr_regex(match)
            abb = match.group(1)
            fullterm = re.search(abR, text)

            if fullterm is not None:
                text = replace(text, abb, fullterm.group(1)[:-1])
            else:
                print('Empty: {0}'.format(abb))
    return text


def clean_str(text):
    """ Some standard text cleaning with regex.
    """
    # Remove unicode characters.
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Combine multiline hyphenated words. Not sure if this is necessary with html.
    text = re.sub('-\s[\r\n\t]+', '', text, flags=re.MULTILINE)
    
    # Remove newlines and extra spaces.
    text = re.sub('[\r\n\t]+', ' ', text, flags=re.MULTILINE)
    text = re.sub('[\s]+', ' ', text, flags=re.MULTILINE)

    return text