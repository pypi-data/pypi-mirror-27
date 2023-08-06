from nose.tools import assert_equal
from pickle_storage import PickleStorage

def test_save_two():
    storage = PickleStorage('lol.pickle')
    storage.put('a', 1)
    storage.put('b', 2)

    assert_equal(2, storage.get('b'))
