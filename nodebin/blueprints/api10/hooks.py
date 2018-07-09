from flask import jsonify

from . import api10
from .exceptions import ApiException


@api10.errorhandler(ApiException)
def platform_not_found_exception(exception):
    return jsonify(exception.to_dict()), exception.status_code
