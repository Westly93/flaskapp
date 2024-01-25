from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskapp.config import Config
from .models import User, db
# app = Flask(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    # migrate = Migrate(app, db)

    from .views import views
    from .creator import creator
    from .student import student   
    from .users.views import auth
    from .errors.handlers import errors

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(creator, url_prefix='/creator')
    app.register_blueprint(student, url_prefix='/student')   
    app.register_blueprint(auth, url_prefix='/users')
    app.register_blueprint(errors)

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('flaskapp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
