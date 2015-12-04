from flask import Blueprint
from neogameserver.models import User, db
from flask_admin.contrib.sqla import ModelView
from flask.ext.login import current_user

adminviews = Blueprint('adminviews', __name__)


class NeoModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()
