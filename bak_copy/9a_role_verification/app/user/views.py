from flask import render_template,request
from flask_login import login_required
from . import user


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



@user.route('/about')
def about():
    return render_template('about.html')
