from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/secret')
def secret():
    return render_template('secret.html')

@main.route('/about')
def about():
    return render_template('about.html')
