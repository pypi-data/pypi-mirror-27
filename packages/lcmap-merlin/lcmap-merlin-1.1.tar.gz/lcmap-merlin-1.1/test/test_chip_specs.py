from merlin import chip_specs as mcs
from merlin.support import data as d


def test_byubid():
    inputs = list()
    inputs.append({'ubid': 'a', 'data': None})
    inputs.append({'ubid': 'b', 'data': None})
    inputs.append({'ubid': 'c', 'data': None})
    results = mcs.byubid(inputs)
    # check that dicts were rekeyed into a new dict
    assert all(map(lambda r: r in results, ['a', 'b', 'c']))
    # check structure of new dict values
    assert all(map(lambda r: 'ubid' in r and 'data' in r, results.values()))


def test_ubids():
    data = ({'ubid': 'a/b/c'}, {'ubid': 'd/e/f'}, {'ubid': 'g'}, {'nope': 'z'})
    good = filter(lambda f: 'ubid' in f, data)
    assert set(map(lambda u: u['ubid'], good)) == set(mcs.ubids(data))


def test_ubids_from_chip_specs():
    assert len(mcs.ubids(d.chip_specs('blue'))) == 4
