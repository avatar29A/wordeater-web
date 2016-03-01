# coding=utf-8
__author__ = 'Warlock'

from flask import Blueprint, render_template
from decorators.authenticate import expose

blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/about')
@expose
def about():
    return render_template("about.html")
