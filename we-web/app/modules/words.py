# coding=utf-8
__author__ = 'Warlock'

from flask import Blueprint, render_template
from decorators.authenticate import requires_auth, expose

blueprint = Blueprint('words', __name__, template_folder='templates')


@blueprint.route('/words/')
@expose
def words():
    return render_template("learning.html")