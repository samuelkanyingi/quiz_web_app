from app import db   # Import the SQLAlchemy instance
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    '''represents a table user in the database 
    inherit from  Usermixin  class to simplify user authentication and gives access to methods and properties
    '''
    id = db.Column(db.Integer, primary_key=True) #unique identifier for user
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(550), nullable=False)
    decks = db.relationship('Deck', backref='owner', lazy=True) # list of deck owned by user/ one to many relationship

class PasswordResetToken(db.Model):
    """Represents a table of password reset token in database.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id  =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(1256), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

class Deck(db.Model):
    '''' represents a table of deck of quizzes in the database '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    quiz_count = db.Column(db.Integer, default=0)
    title = db.Column(db.String(100), nullable=True) #for testing purposes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # represents owner of a deck
    quizzes = db.relationship('Quiz',backref='deck', lazy=True) # list of quizzes associated with a deck

    def to_dict(self):
        ''' Returns dictionary representation of object containing key attributes'''
        return {'id': self.id, 'name': self.name, 'quiz_count': self.quiz_count, 'title': self.title}


class Quiz(db.Model):
    """ Represent a quiz question in database """
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=True) # id of deck it belongs to
    next_review_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow) #next time quiz is to be reviewd
