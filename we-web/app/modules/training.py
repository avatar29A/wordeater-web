# coding=utf-8
__author__ = 'Warlock'

from flask import Blueprint, render_template
from decorators.authenticate import requires_auth, expose

blueprint = Blueprint('training', __name__, template_folder='templates')


@blueprint.route('/training/')
@expose
def training():
    return render_template("training.html")


