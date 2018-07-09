from flask import Blueprint
api10 = Blueprint('api10', __name__)

from . import views
from . import hooks
