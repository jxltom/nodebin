from flask import Blueprint
apiv1 = Blueprint('apiv1', __name__)

from . import views
from . import hooks
