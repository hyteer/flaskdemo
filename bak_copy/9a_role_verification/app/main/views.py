from flask import render_template
from . import main
from flask_login import login_required
from ..decorators import admin_required, permission_required


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/mod')
@login_required
@admin_required
def for_moderators_only():
    return "For comment moderators!"


@main.route('/about')
def about():
    return render_template('about.html')

