from flask import request, jsonify, Response

from nodebin.utils.semver import check_nodesemver_validness
from nodebin.utils.cnpm import cnpm2dict
from ... import PLATFORM_LIST
from .. import api10
from ..exceptions import PlatformNotFoundException, InvalidSemverException


@api10.route('/node/<platform>', defaults={'txt': False})
@api10.route('/node/<platform>.txt', defaults={'txt': True})
def nodejs(platform, txt):
    return _nodejs_view(platform=platform, txt=txt)


@api10.route('/node/<platform>/latest', defaults={'txt': False})
@api10.route('/node/<platform>/latest.txt', defaults={'txt': True})
def nodejs_latest(platform, txt):
    range_ = request.args.get('range', None)
    return _nodejs_view(platform=platform, txt=txt, latest=True, range_=range_)


def _nodejs_view(platform, txt, latest=False, range_=None):
    # Check route validness
    _check_parameter(platform, range_)

    # Prepare response
    rv = cnpm2dict(platform=platform, txt=txt, latest=latest, range_=range_)

    # Output response
    if txt:
        rv = Response(rv)
        rv.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return rv
    return jsonify(rv)


def _check_parameter(platform, range_):
    # Raise exception if platform is not matched
    if platform not in PLATFORM_LIST:
        raise PlatformNotFoundException()

    # Raise exception if range is not valid as a semantic version
    if not check_nodesemver_validness(range_):
        raise InvalidSemverException()

    return True
