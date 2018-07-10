from semantic_version import Version


# TODO: It does not support beta version
# TODO: ^8.1.1 is not supported
def check_nodesemver_validness(nodesemver):
    # Replace x to 0 if x exists
    nodesemver = nodesemver.replace('x', '0')

    # Calculate version parts number
    nodesemver = _padding_nodesemver(nodesemver)

    # Check semantic version validness
    try:
        Version(nodesemver)
    except ValueError:
        return False

    return True


def nodesemver2range(nodesemver):
    """The nodesemver must be valid for using this method.
    8->[8.0.0, 9.0.0)
    8.x->[8.0.0, 9.0.0)
    8.x.1->[8.0.0, 9.0.0)
    8.1.1->[8.1.1, 8.1.2)
    8.1->[8.1.0, 8.2.0)
    """
    low = _remove_x_in_nodesemver(nodesemver)
    high = _increase_nodesemver(low)
    low, high = _padding_nodesemver(low), _padding_nodesemver(high)
    return low, high


def _remove_x_in_nodesemver(nodesemver):
    """8.x->8, 8.x.1->8, 8.x.x->8, 8->8, 8.1.x->8.1, 8.1.1->8.1.1"""
    _ = []
    for e in nodesemver.split('.'):
        if e == 'x':
            break
        _.append(e)

    return '.'.join(_)


def _increase_nodesemver(nodesemver):
    """8.1->8.2, 8->9, 8.1.1->8.1.2"""
    _ = []
    for e in nodesemver.split('.')[:-1]:
        _.append(e)
    _.append(str(int(nodesemver.split('.')[-1]) + 1))

    return '.'.join(_)


def _padding_nodesemver(nodesemver):
    """8->8.0.0, 8.1->8.1.0, 8.1.1->8.1.1"""
    # Calculate version parts number
    num = len(nodesemver.split('.'))

    # Padding .0 if range does not has three parts
    if num < 3:
        nodesemver = nodesemver + '.0' * (3 - num)

    return nodesemver
