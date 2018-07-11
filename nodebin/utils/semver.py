from semantic_version import Version


# TODO: It does not support beta version
# TODO: Tilde range version is not supported
def is_nodesemver_valid(nodesemver):
    # Replace x to 0 if x exists
    nodesemver = nodesemver.replace('x', '0')

    # Remove ^ at the top
    nodesemver = nodesemver.lstrip('^')

    # Padding to 0.0.0 semver format
    nodesemver = _padding_nodesemver(nodesemver)

    # Check semantic version validness
    try:
        Version(nodesemver)
    except ValueError:
        return False

    return True


def nodesemver2range(nodesemver):
    """The nodesemver must be valid for using this method. The returned range
    should be used as [) format. Refer to
    https://docs.npmjs.com/misc/semver#caret-ranges-123-025-004

    8->[8.0.0, 9.0.0)
    8.x->[8.0.0, 9.0.0)
    8.x.1->[8.0.0, 9.0.0)
    8.1.1->[8.1.1, 8.1.2)
    8.1->[8.1.0, 8.2.0)
    ^1.2.3->[1.2.3, 2.0.0)
    ^0.2.3->[0.2.3, 0.3.0)
    ^0.0.3->[0.0.3, 0.0.4)
    ^1.2.x->[1.2.0, 2.0.0)
    ^0.0.x->[0.0.0, 0.1.0)
    ^0.0->[0.0.0, 0.1.0)
    ^1.x->[1.0.0, 2.0.0)
    ^0.x->[0.0.0, 1.0.0)
    """
    # Process x in node semver
    nodesemver = _convert_x_nodesemver(nodesemver)

    # Process node semver to low bound
    low_bound, low_base = _convert_caret_nodesemver(nodesemver)
    low_bound = _padding_nodesemver(low_bound)

    # Process node semver to high bound
    high_bound = _padding_nodesemver(_increase_nodesemver(low_base))

    return low_bound, high_bound


def _convert_x_nodesemver(nodesemver):
    """The basesemver can still have ^ format.
    8.x->8, 8.x.1->8, 8.x.x->8, 8->8, 8.1.x->8.1, 8.1.1->8.1.1, ^8.x->^8
    """
    _ = []
    for e in nodesemver.split('.'):
        if e == 'x':
            break
        _.append(e)

    return '.'.join(_)


def _convert_caret_nodesemver(nodesemver):
    """
     ^1.2.3->[1.2.3, 2.0.0)
    ^0.2.3->[0.2.3, 0.3.0)
    ^0.0.3->[0.0.3, 0.0.4)
    ^1.2->[1.2.0, 2.0.0)
    ^0.0->[0.0.0, 0.1.0)
    ^1->[1.0.0, 2.0.0)
    ^0->[0.0.0, 1.0.0)

    """
    if not nodesemver.startswith('^'):
        return nodesemver, nodesemver

    nodesemver = nodesemver.lstrip('^')
    for i, e in enumerate(nodesemver.split('.')):
        if e == '0':
            if (i + 1) == len(nodesemver.split('.')):
                return nodesemver, '0.' * i + e
        else:
            _ = list(nodesemver.split('.')[0:i])
            _.append(e)
            return nodesemver, '.'.join(_)


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
