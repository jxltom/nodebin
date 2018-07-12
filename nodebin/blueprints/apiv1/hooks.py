from flask import jsonify

from . import apiv1
from .exceptions import ApiException


@apiv1.errorhandler(ApiException)
def api_exception(exception):
    return jsonify(exception.to_dict()), exception.status_code


@apiv1.errorhandler(Exception)
def all_exception(exception):
    return jsonify(dict(code=500, message=str(exception))), 500
