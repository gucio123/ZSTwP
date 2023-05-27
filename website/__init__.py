from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    # pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LDKQWH489312NDKL'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://gutowski:C7xTrPPcz8XefYnt@mysql.agh.edu.pl/gutowski'
    db.init_app(app)

    from .views import views
    from .auth import auth
    import website.create_ticket
    import website.register_contractor
    import website.show_tickets_status
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(create_ticket.bp)
    app.register_blueprint(register_contractor.bp)
    app.register_blueprint(show_tickets_status.bp)

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
