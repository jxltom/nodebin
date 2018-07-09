from flask import Blueprint
app = Blueprint('app', __name__)

from . import views
from . import hooks
from . import models
from . import forms
