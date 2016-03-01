# coding=utf-8
__author__ = 'Warlock'

from flask import Blueprint, render_template
from decorators.authenticate import requires_auth, expose

blueprint = Blueprint('dashboard', __name__, template_folder='templates')

@blueprint.route('/')
@requires_auth
def index():
    return render_template("dashboard.html")


@blueprint.route('/expose')
@expose
def test_expose():
    return "Expose ME! hahaha"
