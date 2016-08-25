from flask import render_template,request
from flask_login import login_required
from . import user
from .. models import User



@user.route('/info')
@login_required
def info():
    #import pdb; pdb.set_trace()
    return render_template('user/info.html')

@user.route('/sec')
@login_required
def secret():
    #import pdb; pdb.set_trace()
    return render_template('user/sec/secret.html')


@user.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        about(404)
    return render_template('user/user.html', user=user)

@user.route('/about')
def about():
    return render_template('about.html')
