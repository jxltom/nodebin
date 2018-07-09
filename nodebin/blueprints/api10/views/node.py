from flask import jsonify, Response

from nodebin.blueprints import PLATFORM_LIST
from nodebin.utils.cnpm import parse_node
from .. import api10
from ..exceptions import PlatformNotFoundException


@api10.route('/node/<platform>', defaults={'ext': ''})
@api10.route('/node/<platform>.txt', defaults={'ext': '.txt'})
def nodejs(platform, ext):
    # Check route validness
    _check_parameter(platform, ext)

    # Prepare response
    rv = parse_node(platform, ext)

    # Output response
    if ext == '':
        return jsonify(rv)
    elif ext == '.txt':
        rv = Response(rv)
        rv.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return rv


@api10.route('/node/<platform>/latest', defaults={'ext': ''})
@api10.route('/node/<platform>.txt/latest', defaults={'ext': '.txt'})
def nodejs_latest(platform, ext):
    # Check route validness
    _check_parameter(platform, ext)

    # Prepare response
    rv = parse_node(platform, ext)

    # Output response
    if ext == '':
        return jsonify(rv)
    elif ext == '.txt':
        return rv


def _check_parameter(platform, ext):
    # Raise exception if platform is not matched
    if platform not in PLATFORM_LIST:
        raise PlatformNotFoundException()

    # Raise exception if extension is not emtpy or .txt
    if ext != '' and ext != '.txt':
        raise PlatformNotFoundException()

    return True
