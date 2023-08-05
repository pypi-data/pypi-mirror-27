# coding: utf-8
from flask import Blueprint, render_template

bp = Blueprint('documentation', __name__)


@bp.route('/documentation')
def get_docs():
    """Help pages and documentation

    :returns html_template index.html:
    """
    return render_template('docs/index.html')