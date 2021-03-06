from datetime import datetime
from flask import render_template,session,redirect,url_for,current_app

from . import main
from .forms import NameForm
from .. import db
from ..emails import send_email
from ..models import User



@main.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            print "new user <%s> visited." % user
            if current_app.config['YT_ADMIN']:
                send_email(current_app.config['YT_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        print "user <%s> visited." % form.name.data
        form.name.data = ''

        return redirect(url_for('.index'))
    return render_template('index.html',form=form,name=session.get('name'),
           known=session.get('known',False),current_time=datetime.utcnow())



