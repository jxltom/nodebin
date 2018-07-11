from flask import jsonify

from . import apiv1
from .exceptions import ApiException


@apiv1.errorhandler(ApiException)
def platform_not_found_exception(exception):
    return jsonify(exception.to_dict()), exception.status_code
