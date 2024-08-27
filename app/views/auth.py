from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from app.models import User, db
from app import login_manager
from app import bcrypt
from app import serializer #serializer helps you generate tokens
from app import hashlib #store token securely 
from app import datetime, timedelta
from app import jsonify
from app.models import PasswordResetToken
from app.controllers import send_reset_email

auth_bp =  Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' route to handle http request for a user signup '''
    if request.method == 'POST':
        #extract values from request form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Received signup data: Username={username}, Email={email}, Password={password}")  # i used this line for debugging
        #checks if user existing with same email or email
        existing_person = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_person:
            flash('username or email already exist.Please chose a different one', 'danger')
            return render_template('index.html')
        #if no username or email found hash passowrd using bcrypt library
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        #create a new instance of to represent user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup success! Try login in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('index.html') # GET request

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    ''' checks for http request for login route '''
    if request.method == 'POST':
        # retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Attempting login with email: {email}") #for debugging
        print(f"Provided password: {password}") # for debugging

        # query database for a user with specified email address filter by email and return first user found
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password): #hash passwords and compare
            login_user(user) # stores user info in a session  
            flash('Login success', 'success')
            print('Login success') #debugging line
            return redirect(url_for('user.home')) 
        else:
            flash('Invalid credentials', 'danger')
            return render_template('index.html')
    else:
        return render_template('index.html') # GET request to login route

#logout user
@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    ''' function that logs out user from a session '''
    logout_user() #removes user session meaning user will need to authnticate to log in again
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.landing_page'))


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    #check if user exists
    if user:
        token = serializer.dumps(email, salt='password-reset-salt') #generate unique token
        hashed_token = hashlib.sha256(token.encode()).hexdigest() #hash the token

        #store hashed token in database with expiration time
        expiration_time = datetime.now() + timedelta(hours=1)
        reset_token = PasswordResetToken(user_id=user.id, token=hashed_token, expires_at=expiration_time)  #creates a new instance of PasswordResetToken
        db.session.add(reset_token)
        db.session.commit()

        #send email with token
        reset_link = url_for('auth.reset_password', token=token, _external=True) #generated full url with domain name included
        send_reset_email(user.email, reset_link) #function to send email to user with passowrd reset link
    return jsonify({'message': 'An email has been sent if it exist in our system'})


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        #load email from token using serializer.loads
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600) #salt adds security
    except Exception as e:
        return 'The reset link is invalid or has expired', 400 #error message reason likely is token expired or is invalid
    if request.method == 'POST':
        new_password = request.form.get('password')

        confirm_password = request.form.get('confirm_password')

        #hash new_password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        user = User.query.filter_by(email=email).first() #retrieve user object from database
        if user:
            user.password = hashed_password #updates to new password
            db.session.commit()
            flash('Your password has been successfully updated', 'success')
            return redirect(url_for('auth.login'))
        else:
            return 'User not found', 404
    return render_template('reset_password.html', token=token)
