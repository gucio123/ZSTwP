from flask import Flask
<<<<<<< Updated upstream
# from models import User
=======

# import pymysql

>>>>>>> Stashed changes
# from os import path
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
<<<<<<< Updated upstream
=======

    # pymysql.install_as_MySQLdb()

>>>>>>> Stashed changes
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LDKQWH489312NDKL'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://gutowski:C7xTrPPcz8XefYnt@mysql.agh.edu.pl/gutowski'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')


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
