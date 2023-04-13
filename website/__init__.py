from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager 

# define a new database object
db = SQLAlchemy()
# set a name for the database
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    # telling Flask that the database is located at this location; f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initializing the database
    db.init_app(app)

    from .views import views
    from .auth import auth

    ## regestering the blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    ## importing the needed classes; User & Note
    from .models import User, Note

    ## calling the create_database Function to create a DB if not existed
    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  ## flask will redirect us to 'auth.login' if we are not logged-in
    login_manager.init_app(app)  ## telling the login_manager which app we are using, i.e., configure the app for login.


    ## providing a user_loader callback.
    ## This callback is used to reload the user object from the user ID stored in the session.
    ## It should take the unicode ID of a user, and return the corresponding user object.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  ## look for the primary key

    return app


## check if the database exists or not. if not => create the database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')







