# encoding:utf-8
'''
    Flask Demo App
    By: YT
    2016.8
'''
import os
from datetime import datetime
from flask import Flask, redirect,session, abort, render_template,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


from model import Users
from model.users import load_user

#### App initializing ####
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

#### Config ####
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'my secret string'

db = SQLAlchemy(app)


#### Form Class ####
class NameForm(Form):
    name = StringField('What is your anme?',validators=[DataRequired()])
    submit = SubmitField('Submit')

#### Model ####
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

#### Def Routes ####

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        print "%s Requested."%session.get('name')
        return redirect(url_for('index'))

    return render_template('index.html',form=form,name=session.get('name'),current_time=datetime.utcnow())

@app.route('/user/<name>')
def userboot(name):
    return render_template('user.html',title="User",name=name)

### Jinja2 Templates test
@app.route('/temptest')
def temptest():
    dict1 = {'key':1111,'name':'Tony'}
    list1 = ['aaa','bbb','ccc']
    test = "<h3>a variable</h3>"
    test2 = "another variable"

    obj = load_user(2)
    return render_template('temptest.html',mydict=dict1,mylist=list1,myobj=obj,myintvar=1,test=test,test2=test2,comments=list1)

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

#### Special Routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()

