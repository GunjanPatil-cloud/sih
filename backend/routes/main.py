"""Main routes — landing page and static pages."""

from flask import Blueprint, render_template
from database.db import check_connection

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page."""
    db_status = check_connection()
    return render_template('index.html', db_status=db_status)


@main_bp.route('/about')
def about():
    """About page — project information."""
    return render_template('about.html')
