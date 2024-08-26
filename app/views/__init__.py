from .contact import contact_bp #imports blueprint instance from contact.py
from .auth import auth_bp
from .deck import deck_bp
from .quiz import quiz_bp
from .user import user_bp

def register_views(app):
    ''' function to register imported blueprints with flask app'''
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(deck_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(user_bp)