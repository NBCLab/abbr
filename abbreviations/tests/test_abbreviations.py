from .utils import get_test_data_path
from abbreviations.abbreviations import findall, expandall, clean_str
from glob import glob
from os.path import join
import cPickle as pickle


def test_findall():
    data_dir = get_test_data_path()
    files = glob(join(data_dir, 'raw*.txt'))
    
    for f in files:
        pkl_file = f.replace('raw_', '').replace('.txt', '.pkl')
        with open(f, 'rb') as fo:
            text = fo.read()
        
        text = clean_str(text)
        d = findall(text)
        d = {k: v for (k, v) in d.items() if v is not None}
        
        with open(pkl_file, 'rb') as fo:
            d2 = pickle.load(fo)
        
        assert d == d2


def test_expandall():
    data_dir = get_test_data_path()
    files = glob(join(data_dir, 'raw*.txt'))
    
    for f in files:
        exp_file = f.replace('raw', 'expanded')
        with open(f, 'rb') as fo:
            test_text = fo.read()
        
        with open(exp_file, 'rb') as fo:
            exp_text = fo.read()
        
        test_text = clean_str(test_text)
        exp_text = clean_str(exp_text)

        test_text = expandall(test_text)
        
        assert test_text==exp_text
