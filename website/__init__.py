from flask import Flask
# import pymysql
# from models import User
# from os import path
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LDKQWH489312NDKL'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://gutowski:C7xTrPPcz8XefYnt@mysql.agh.edu.pl/gutowski'

    # Production database, don't use until needed
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://mikolek:gCe1Zn893jk7Awun@mysql.agh.edu.pl/mikolek'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://gutowsk2:2xgPg28fNcAWyhSG@mysql.agh.edu.pl/gutowsk2'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .views import fault_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(fault_bp, url_prefix='/faults')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')
