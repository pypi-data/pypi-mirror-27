import requests

def get(query):
    """Queries aardvark and returns chip_specs

    Args:
        query (str): full url query for aardvark

    Returns:
        tuple: sequence of chip specs

    Example:
        >>> chip_specs.get('http://host/v1/landsat/chip-specs?q=red AND sr')
        ('chip_spec_1', 'chip_spec_2', ...)
    """

    return tuple(requests.get(query).json())


def getmulti(queries):
    """Queries urls and returns chip_specs organized by key

    Args:
        queries (dict): {'key1': 'url', 'key2': 'url2}

    Example:
        >>> chip_specs.getmulti({'red':  'http://host/v1/landsat/chip-specs?q=red AND sr',
                                 'blue': 'http://host/v1/landsat/chip-specs?q=blue AND sr'})
        {'red': (red_spec_1, red_spec_2, ...), 'blue': (blue_spec_1, blue_spec_2)}
    """

    return {k: get(v) for k, v in queries.items()}


def byubid(chip_specs):
    """Organizes chip_specs by ubid

    Args:
        chip_specs (sequence): a sequence of chip specs

    Returns:
        dict: chip_specs keyed by ubid
    """

    return {cs['ubid']: cs for cs in chip_specs}


def ubids(chip_specs):
    """Extract ubids from a sequence of chip_specs

    Args:
        chip_specs (sequence): a sequence of chip_spec dicts

    Returns:
        tuple: a sequence of ubids
    """

    return tuple(cs['ubid'] for cs in chip_specs if 'ubid' in cs)
