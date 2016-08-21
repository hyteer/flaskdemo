from flask import render_template,request
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/secret')
def secret():
    import pdb; pdb.set_trace()
    return render_template('user/sec/secret.html')

@main.route('/about')
def about():
    return render_template('about.html')

#### Special Routes
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500