from os.path import dirname, join, abspath


def get_test_data_path():
    """ Returns the path to test datasets.
    """
    return abspath(join(dirname(__file__), 'data'))
