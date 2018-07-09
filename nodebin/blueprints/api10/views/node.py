from flask import jsonify

from nodebin.utils.cnpm import parse
from .. import api10


@api10.route('/node/linux-x64')
def linux():
    return jsonify(parse())
