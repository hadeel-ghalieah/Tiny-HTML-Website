from . import db

from flask_login import UserMixin
## UserMixin provides default implementations for the methods that
##          Flask-Login expects user objects to have.

from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    
    ## adding date automatically
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    ## assosiating NOTES to users
    ## one-to-many relationship; 1 User has Multiple NOTES
    ## 'user.id is the primary key for the object we are referencing
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) ## unique id for the object

    ## no user can have the same email as another user
    email = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))  ## 150 characters 
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') 
