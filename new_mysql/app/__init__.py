#coding:utf8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_pagedown import PageDown
from . mysql_model import Mysql

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

#conn,cur = mydb.connDB()



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

class FlaskApp:
    mydb = None
    conn = None
    cur = None

    def create_app(self,config_name):
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)

        bootstrap.init_app(app)
        mail.init_app(app)
        moment.init_app(app)
        db.init_app(app)
        login_manager.init_app(app)
        pagedown.init_app(app)
        FlaskApp.mydb = Mysql()
        FlaskApp.mydb.init_app(app)
        FlaskApp.conn = FlaskApp.mydb.conn
        FlaskApp.cur = FlaskApp.mydb.cur




        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .user import user as user_blueprint
        app.register_blueprint(user_blueprint, url_prefix='/user')

        from .api_1_0 import api as api_1_0_blueprint
        app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

        return app

    def __del__(self):
        if self.mydb:
            print u"应用退出，准备关闭数据库连接..."
            self.mydb.connClose()
            print u"关闭成功!"
        else:
            pass
