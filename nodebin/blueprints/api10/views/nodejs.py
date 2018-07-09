from flask import jsonify

from nodebin.blueprints import PLATFORM_LIST
from nodebin.utils.cnpm import parse
from .. import api10
from ..exceptions import PlatformNotFoundException


@api10.route('/node/<platform>', defaults={'ext': ''})
@api10.route('/node/<platform>.txt', defaults={'ext': '.txt'})
def nodejs(platform, ext):
    # Raise exception if platform is not matched
    if platform not in PLATFORM_LIST:
        raise PlatformNotFoundException()

    # Raise exception if extension is not emtpy or .txt
    if ext != '' and ext != '.txt':
        raise PlatformNotFoundException()

    return jsonify(parse(platform, ext))


@api10.route('/node/<platform>/latest', defaults={'ext': ''})
@api10.route('/node/<platform>.txt/latest', defaults={'ext': '.txt'})
def nodejs_latest(platform, ext):
    return jsonify(parse())
