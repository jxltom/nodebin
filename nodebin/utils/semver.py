from semantic_version import Version


# TODO: It does not support beta version
def check_nodesemver_validness(nodesemver):
    # Convert range to version
    semver = _nodesemver2semver(nodesemver)

    # Check semantic version validness
    try:
        Version(semver)
    except ValueError:
        return False

    return True


def range2version(range_):
    """Return minimal  """
    pass


def _nodesemver2semver(nodesemver):
    """The returned semver may be invalid such as 8.x.x.x will be 8.0.0.0"""
    # Replace x to 0 if x exists
    semver = nodesemver.replace('x', '0')

    # Calculate version parts number
    parts_num = len(semver.split('.'))

    # Padding .0 if range does not has three parts
    if parts_num < 3:
        semver = semver + '.0' * (3 - parts_num)

    return semver
