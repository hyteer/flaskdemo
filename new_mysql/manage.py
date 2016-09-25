#!/usr/bin/env python
import os
from app import FlaskApp, db
from app.models import User, Role,Permission, Post, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


flaskapp = FlaskApp()
app = flaskapp.create_app(os.getenv('FLASK_CONFIG') or 'default')
mydb = FlaskApp.mydb
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post,
                Follow=Follow, Comment=Comment, mydb=mydb)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
