from cytoolz import first
from cytoolz import partial
from cytoolz import second
from merlin import chips
from merlin import chip_specs


def chips_and_specs(point, acquired, keyed_specs, chips_fn):
    """Returns chips and specs for a dict of specs
    
    Args:
        point: (tuple): (x, y) which is within the extents of a chip
        acquired: (str): ISO8601 date range
        keyed_specs: (dict): {key: [spec1, spec2,], key2: [spec3, spec4]}
        chips_fn (function): Accepts x, y, acquired, ubids.  Returns chips.

    Returns:
        dict: {key: (chips, specs), key2: (chips, specs), ...}
    """
    chips = partial(chips_fn, x=first(point), y=second(point), acquired=acquired)
    return {k: (chips(ubids=chip_specs.ubids(v)), v) for k, v in keyed_specs.items()}


def locate(point, spec):
    """Returns chip_x, chip_y and all chip locations given a point and spec

    Args:
        point (sequence): sequence of x,y
        spec (dict): chip spec

    Returns:
        tuple: (chip_x, chip_y, chip_locations), where chip_locations is a
        two dimensional chip-shaped numpy array of (x,y)
    """
    chip_x, chip_y = chips.snap(*point, chip_spec=spec)
    chip_locations = chips.locations(chip_x, chip_y, spec)
    return (chip_x, chip_y, chip_locations)
