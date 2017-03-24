from .utils import get_test_data_path
from ..utils import get_res, do_words_match, replace, make_abbr_regex
from glob import glob
from os.path import join
import json

def test_do_words_match():
    w1 = 'stemming'
    w2 = 'stem'
    assert do_words_match(w1, w2)

def test_replace():
    in_text = 'This is a TS'
    abb = 'TS'
    fullterm = 'test string'
    true = 'This is a test string'
    test = replace(in_text, abb, fullterm)
    assert test == true
