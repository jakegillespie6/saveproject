from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#create a variable for our database
db = SQLAlchemy()
DB_NAME = "database.db"

#defining our function of instantation our flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sleeper123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    #import our endpoint functions
    from .views import views
    from .auth import auth

    #register blueprints for views and auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.config['UPLOAD_FOLDER'] = 'Flask Web App\website\static'
    #importing our database models
    from .models import User, Ticket

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    #instantiate our database
    create_database(app)

    return app

#check if the database exists in our directory, if not create a database
def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

