from flask import request, jsonify, Response
from semantic_version import Version

from nodebin.utils.semver import check_nodesemver_validness
from nodebin.utils.cnpm import cnpm2data
from ... import PLATFORM_LIST
from .. import api10
from ..exceptions import (
    PlatformNotFoundException, InvalidSemverException, NoResultException
)


@api10.route('/node/<platform>', defaults={'txt': False})
@api10.route('/node/<platform>.txt', defaults={'txt': True})
def nodejs(platform, txt):
    return _nodejs_view(platform=platform, txt=txt)


@api10.route('/node/<platform>/latest', defaults={'txt': False})
@api10.route('/node/<platform>/latest.txt', defaults={'txt': True})
def nodejs_latest(platform, txt):
    nodesemver = request.args.get('range', None)
    return _nodejs_view(
        platform=platform, txt=txt, latest=True, nodesemver=nodesemver
    )


def _nodejs_view(platform, txt, latest=False, nodesemver=None):
    # Check route validness
    _check_parameter(platform, nodesemver)

    # Prepare response
    data = cnpm2data(platform=platform, nodesemver=nodesemver)

    # Raise exception if no result is found
    if not data:
        raise NoResultException()

    # Postprocess data
    data = _postprocess_data(data=data, latest=latest, txt=txt)

    # Output response
    if txt:
        rv = Response(data)
        rv.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return rv
    return jsonify(data)


def _check_parameter(platform, nodesemver):
    # Raise exception if platform is not matched
    if platform not in PLATFORM_LIST:
        raise PlatformNotFoundException()

    # Raise exception if range is not valid as a semantic version
    if nodesemver is not None and not check_nodesemver_validness(nodesemver):
        raise InvalidSemverException()

    return True


def _postprocess_data(data, latest, txt):
    # Filter by latest
    if latest:
        data = sorted(data, key=lambda d: Version(d['number']), reverse=True)[0]

    # Output response
    if txt:
        # Convert to list first if latest para only returns one
        data = [data] if type(data) is dict else data
        # Convert to strings
        data = '\n'.join(['{} {}'.format(d['number'], d['url']) for d in data])

    return data
