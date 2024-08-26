from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_bcrypt import Bcrypt
import hashlib #store password securely on database
from .config import Config #import config from current directory

#instances
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login" # page to redirect users when they are not logged in
serializer = URLSafeTimedSerializer(app.secret_key) #generates token

from .views import *  # Import routes and view functions
from app.models import User
from app.views.auth import auth_bp
from app.views.contact import contact_bp
from app.views.deck import deck_bp
from app.views.quiz import quiz_bp
from app.views.user import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(deck_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(user_bp)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
