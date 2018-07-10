from semantic_version import Version


# TODO: It does not support beta version
def check_range_validness(range_):
    # Replace x to 0 if x exists
    range_ = range_.replace('x', '0')

    # Calculate version parts number
    parts_num = len(range_.split('.'))

    # Return invalid if there are more than three parts
    if parts_num > 3:
        return False

    # Padding .0 if range does not has three parts
    if parts_num != 3:
        range_ = range_ + '.0' * (3 - parts_num)

    # Check semantic version validness
    try:
        Version(range_)
    except ValueError:
        return False

    return True


def range2version(range_):
    """Return minimal  """
    pass
