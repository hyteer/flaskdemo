# encoding:utf-8
'''
This script could be run with commands
'''

from flask import Flask, redirect, abort, render_template
from flask_script import Manager

from DemoLib import Users
from DemoLib.users import load_user

app = Flask(__name__)
manager = Manager(app)


#### Def Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',title="User",name=name)


### Jinja2 Templates test
@app.route('/temptest')
def temptest():
    dict1 = {'key':1111,'name':'Tony'}
    list1 = ['aaa','bbb','ccc']
    test = "<h3>a variable</h3>"
    test2 = "another variable"
    obj = load_user(2)
    return render_template('temptest.html',mydict=dict1,mylist=list1,
                           myobj=obj,myintvar=1,test=test,test2=test2,comments=list1)

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


@app.route('/bad')
def bad():
    return 'Bad request.',400
####
#url_for('static', filename='css/styles.css', _external=True)



#### Special Routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()

