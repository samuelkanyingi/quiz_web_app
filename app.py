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

app = Flask(__name__, static_folder='static')
app.secret_key = 'sammy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/quiz_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'samuelkanyingi2016@gmail.com'
app.config['MAIL_PASSWORD'] = 'tkih fuut pegn eyuw'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
serializer = URLSafeTimedSerializer(app.secret_key) #generates token


current_question_index = 0 


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

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

with app.app_context():
    db.create_all()

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        subject = request.form['subject']
        email = request.form['email']
        message = request.form['message']

        #create an email message
        msg = Message(subject, sender=email,
                      recipients=['samuelkanyingi2016@gmail.com'])
        msg.body = f'Message from {email}\n\n {message}'

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash('Message  failed to send.Please try again later.', 'error')
            return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Received signup data: Username={username}, Email={email}, Password={password}")
        existing_person = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_person:
            flash('username or email already exist.Please chose a different one', 'danger')
            return render_template('index.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        #create a new instance or new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup success! Try login in', 'success')
        return redirect(url_for('login'))
    return render_template('index.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Attempting login with email: {email}")
        print(f"Provided password: {password}")

        # query databse for user credentials
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login success', 'success')
            print('Login success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
            #return redirect(url_for('login'))
            return render_template('index.html')
    else:
        return render_template('index.html')

#logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing_page'))


def get_current_question():
    current_question = Quiz.query.order_by(Quiz.id.desc()).first()
    if current_question:
        return current_question
    return None


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    #check if user exists
    if user:
        token = serializer.dumps(email, salt='password-reset-salt')
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        #store hashed token in database with expiration time

        expiration_time = datetime.now() + timedelta(hours=1)
        reset_token = PasswordResetToken(user_id=user.id, token=hashed_token, expires_at=expiration_time)
        db.session.add(reset_token)
        db.session.commit()

        #send email with token
        reset_link = url_for('reset_password', token=token, _external=True)
        send_reset_email(user.email, reset_link)
    return jsonify({'message': 'An email has been sent if it exist in our system'})

def send_reset_email(to_email, reset_link):
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[to_email])
    msg.body = f''' To reset your password, Visit link below: {reset_link}
    Password expires after 1 hour. if you did not make this request simply ignore this email'''
    mail.send(msg)
    print(f'Send this link to {to_email}: {reset_link}')

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        return 'The reset link is invalid or has expired', 400
    if request.method == 'POST':
        new_password = request.form.get('password')

        confirm_password = request.form.get('confirm_password')

        #hash password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been successfully updated', 'success')
            return redirect(url_for('login'))
        else:
            return 'User not found', 404
    return render_template('reset_password.html', token=token)


@app.route('/get_current_question_id', methods=['GET'])
def get_current_question_id():
    # Assuming you have a method to get the current question ID from the session or other logic
    current_question = get_current_question()  # Implement this method to fetch the current question
    if current_question:
        return jsonify({'id': current_question.id})
    else:
        return jsonify({'error': 'No current question found'}), 404


@app.route('/update_next_review_time', methods=['POST'])
def update_next_review_time():
    print("Received POST request to /update_next_review_time")
    data = request.get_json()
    
    print(f"Received data: {data}")
    question_id = data.get('id')  
    print("Question ID (integer):", question_id)
    
  
    delay_time = data.get('delay_time') # convert to integer
    print(f"Received data converted: {data}")
 
    #calculate next review
    next_review_time = datetime.now() + timedelta(milliseconds=delay_time)

    #fetch quiz question by ID
    quiz = Quiz.query.get(question_id)
    print(f"Question ID: {question_id}")

    if quiz:
        quiz.next_review_time = next_review_time
        db.session.commit()
        print(f"Updated next review time for question ID {question_id} to {quiz.next_review_time}")
        return jsonify(success=True, message='Next review time updated successfully')
    else:
        return jsonify(success=False, message='Quiz not found'), 404

@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/home')
@login_required  # Ensure the user is logged in
def home():
    user = current_user  # Get the currently logged-in user
    decks = Deck.query.filter_by(user_id=user.id).all() # Get decks for the current user
    deck_data = []

    # get current date
    current_date = datetime.utcnow().date()

    # prepare data for each deck
    if decks:
        for deck in decks:
            quiz_count = Quiz.query.filter_by(deck_id=deck.id).count()
            due_quiz_count = Quiz.query.filter(
                Quiz.deck_id == deck.id,
                Quiz.next_review_time <= datetime.utcnow()
            ).count()
            deck_data.append({
                'id': deck.id,
                'title': deck.title,
                'quiz_count': quiz_count,
                'due_quiz_count': due_quiz_count
            })
        print(f"Retrieved {len(decks)} decks from the database")
    else:
        flash("You have no decks.Please add a new deck")
    
    return render_template('home.html', decks=deck_data)


@app.route('/add_deck', methods=['POST'])
@login_required
def add_deck():
    if request.method == 'POST':
        print("Received POST request for adding a deck")
        title = request.form['title']
        print(f"Received title: {title}")
        # Create a new deck object
        new_deck = Deck(title=title, name='Default Name', quiz_count=0, user_id=current_user.id)
        db.session.add(new_deck)
        db.session.commit()
    
        flash('Deck created successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('home.html')



@app.route('/delete_deck/<int:deck_id>', methods=['POST', 'DELETE'])
def delete_deck(deck_id):
    deck_to_delete = Deck.query.get_or_404(deck_id)
    db.session.delete(deck_to_delete)
    db.session.commit()

    return jsonify({'success': True}), 200

@app.route('/edit_deck', methods=['POST'])
def edit_deck():
    # Retrieve deck ID and new title from the form data
    deck_id = request.form.get('deck_id')
    new_title = request.form.get('title')

    if deck_id and new_title:
        # Query the deck from the database using the deck_id
        deck = Deck.query.get(deck_id)
        if deck:
            deck.title = new_title
            db.session.commit()
            flash('Deck updated successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/deck/<int:deck_id>', methods=['GET'])
def deck_page(deck_id):
    deck = Deck.query.get_or_404(deck_id) 
    quizzes = Quiz.query.filter_by(deck_id=deck_id).all()    
    return render_template('deck_page.html', deck=deck, quizzes=quizzes)


@app.route('/decks')
def get_decks():
    decks = Deck.query.all()
    return render_template('home.html', decks=decks)

@app.route('/get_decks')
def get_deck():
    decks = Deck.query.all()
    decks_list = [deck.to_dict() for deck in decks]
    return jsonify(decks_list), 200

@app.route('/decks', methods=['POST'])
def create_deck():
    data = request.get_json()
    new_deck = Deck(name=data['name'], quiz_count=data['quiz_count'])
    db.session.add(new_deck)
    db.session.commit()
    return jsonify(new_deck.to_dict()), 201

@app.route('/decks/<int:deck_id>', methods=['PUT'])
def update_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({'error': 'Deck not found'}), 404

    data = request.get_json()
    deck.name = data['name']
    deck.quiz_count = data['quiz_count']
    db.session.commit()
    return jsonify(deck.to_dict())

@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    deck_id = request.form.get('deck_id')
    question = request.form.get('question')
    answer = request.form.get('answer')

    print("Received form data:", request.form)
    print("deck_id:", deck_id)
    print("question:", question)
    print("answer:", answer)

    if 'deck_id' in request.form and 'question' in request.form and 'answer' in request.form:
        deck_id = request.form['deck_id']
        question = request.form['question']
        answer = request.form['answer']
        new_quiz = Quiz(deck_id=deck_id, question=question, answer=answer)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('deck_page', deck_id=deck_id))
    else:
        return "Error: missing form data"

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('deck_page', deck_id=quiz.deck_id))

@app.route('/edit_quiz', methods=['POST'])
def edit_quiz():
    # Retrieve form data
    quiz_id = request.form.get('quiz_id')
    question = request.form.get('question')
    answer = request.form.get('answer')

    if not quiz_id or not question or not answer:
        return "Error: Missing form data", 400  # Return an error if required data is missing

    # Find the quiz to be updated
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Error: Quiz not found", 404  # Return an error if the quiz is not found

    # Update the quiz details
    quiz.question = question
    quiz.answer = answer

    db.session.commit()

    # Redirect to the page displaying the deck with the updated quizzes
    return redirect(url_for('deck_page', deck_id=quiz.deck_id))

@app.route('/get_next_question', methods=['GET'])
def get_next_question():
    global current_question_index
    print(f"Current question index: {current_question_index}")
    # Fetch all questions, assuming they are ordered by id
    questions = Quiz.query.all()

    # Check if there are any more questions available
    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        current_question_index += 1  # Move to the next question
        return jsonify({
            'question': next_question.question,
            'id': next_question.id,
            'total_questions': len(questions)
        })
    else:
        print("No more questions available")  # Debugging line
   

if __name__ == '__main__':
    app.run(debug=True)
