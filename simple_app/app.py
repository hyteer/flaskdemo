# encoding:utf-8
'''
    Flask Demo App
    By: YT
    2016.8
'''
import os
from datetime import datetime
from flask import Flask, redirect,session, abort, render_template,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message

from model import Users
from model.users import load_user

##### App initializing #####
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


######### Config ###########
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'my secret string'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#### Mail
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
#app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'hyteer@qq.com'
#app.config['MAIL_PASSWORD'] = 'rvkxxmswbjeseabj'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

app.config['YT_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['YT_MAIL_SENDER'] = 'YT Flask <hyteer@qq.com>'
app.config['YT_ADMIN'] = 'yotong@qq.com'
#app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


####### Shell commands ######
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)




######## Form Class #########
class NameForm(Form):
    name = StringField('What is your anme?',validators=[DataRequired()])
    submit = SubmitField('Submit')

########## Model ############
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

########### Mail #############
def send_email(to,subject,template, **kwargs):
    msg = Message(app.config['YT_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['YT_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

########## Def Routes ########

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            print "new user <%s> visited." % user

            if app.config['YT_ADMIN']:
                send_email(app.config['YT_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        print "user <%s> visited." % form.name.data
        form.name.data = ''

        return redirect(url_for('index'))
    return render_template('index_db.html',form=form,name=session.get('name'),
           known=session.get('known',False),current_time=datetime.utcnow())

@app.route('/user/<name>')
def userboot(name):
    return render_template('user.html',title="User",name=name)

###### Jinja2 Templates test #####
@app.route('/temptest')
def temptest():
    dict1 = {'key':1111,'name':'Tony'}
    list1 = ['aaa','bbb','ccc']
    test = "<h3>a variable</h3>"
    test2 = "another variable"

    obj = load_user(2)
    return render_template('temptest.html',mydict=dict1,mylist=list1,myobj=obj,
                           myintvar=1,test=test,test2=test2,comments=list1)

@app.route('/temptest/<int:id>')
def get_user(id):
    print "Get user id:",id
    user = load_user(id)
    #if not user:
        #abort(404)
    return render_template('temptest_user.html',user=user)


@app.route('/tempext')
def tempextend():
    return render_template('temp_ext.html')


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bad')
def bad():
    return 'Bad request.',400

######### Special Routes ########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()

