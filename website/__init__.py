from flask import Flask
# from models import User
# from os import path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
# from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LDKQWH489312NDKL'
    engine = create_engine('mysql://gutowski:C7xTrPPcz8XefYnt@mysql.agh.edu.pl/gutowski')
    Base = declarative_base()
    Base.metadata.reflect(engine)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     from .models import User
    #     return User.query.get(int(id))

    return app
