from flask import render_template,request
from . import user


@user.route('/info')
def info():
    #import pdb; pdb.set_trace()
    return render_template('user/info.html')

@user.route('/sec')
def secret():
    #import pdb; pdb.set_trace()
    return render_template('user/sec/secret.html')

@user.route('/about')
def about():
    return render_template('about.html')
