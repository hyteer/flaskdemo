from flask import Flask, redirect, abort
app = Flask(__name__)

from DemoLib import Users
from DemoLib.users import load_user

#### Def methods

def do_the_login():
        print "You've posted a login request."
        return "Hi,you've posted a login request."
def show_the_login_form():

    print 'Hello, please login.'
    return '<h2>Hi,please login.</h2>'


#### Def Routes

@app.route('/')
def index():
    return '<h1>Demo Home</h1>'

@app.route('/test')
def test():
    return 'Test....'

@app.route('/red')
def red():
    return redirect('http://www.ifcld.com')

@app.route('/user/<int:id>')
def get_user(id):
    print "Get user id:",id
    user = load_user(id)
    if not user:
        abort(404)
    return '<h2>Hello, %s !' % user.name

@app.route('/bad')
def bad():
    return 'Bad request.',400

user = load_user(2)
print user.name
print Users.name

if __name__ == '__main__':
    app.run(debug=True,port=8000)