from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__, static_folder='static')
app.secret_key = 'sammy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/quiz_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
 

current_question_index = 0 
total_score = 0

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    quiz_count = db.Column(db.Integer, default=0)
    title = db.Column(db.String(100), nullable=True)
    quizzes = db.relationship('Quiz',backref='deck', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'quiz_count': self.quiz_count, 'title': self.title}


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    #title = db.Column(db.String(100), nullable=False)
# quiz = Quiz.query.first()
# print(quiz.deck.title)  # Accessing the title of the related deck

# with app.app_context():
#     db.create_all()
@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/login')
def get_message():
    return render_template('index.html', message="hello quiz app")

@app.route('/home')
def home():
    decks = Deck.query.all()
    print(f"Retrieved {len(decks)} decks from the database")
    
    return render_template('home.html', decks=decks)


@app.route('/add_deck', methods=['POST'])
def add_deck():
    title = request.form['title']

    # Create a new deck object
    new_deck = Deck(title=title, name='Default Name', quiz_count=0)
    db.session.add(new_deck)
    db.session.commit()
    
    #return jsonify({'message': 'deck created successfully'}), 201
    #return render_template('home.html')
    return redirect(url_for('home'))

# @app.route('/add_deckz', methods=['POST'])
# def add_decck():
#     if request.method == 'POST':
#         data = request.get_json()
#         print(f"Received data: {data}")  # Log the received data
#         name = data.get('name')
#         quiz_count = data.get('quiz_count')
#         deck = Deck(name=name, quiz_count=quiz_count)
#         db.session.add(deck)
#         db.session.commit()
#         # return jsonify(new_deck.to_dict()), 201
#         print(f"Deck added with ID: {deck.id}")
#         return jsonify({'message': 'deck created successfully'}), 201
#     elif request.method == 'GET':
#         decks = Deck.query.all()
#         return jsonify([{'id':deck.id, 'name': deck.name, 'quiz_count': quiz_count} for deck in decks])


@app.route('/delete_deck/<int:deck_id>', methods=['POST'])
def delete_deck(deck_id):
    deck_to_delete = Deck.query.get_or_404(deck_id)
    db.session.delete(deck_to_delete)
    db.session.commit()

    # Redirect to the home page after deletion
    return redirect(url_for('home'))

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
    deck = Deck.query.get_or_404(deck_id)  # Assuming Deck is your model
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

@app.route('/api/quizzes/<int:deck_id>')
def get_quizzes(deck_id):
    quizzes = Quiz.query.filter_by(deck_id=deck_id).all()
    return jsonify([{
        'id': quiz.id,
        'question': quiz.question,
        'answer': quiz.answer
    } for quiz in quizzes
    ])
# @app.route('/decks/<int:deck_i>', methods=['POST','DELETE'])
# def delete_deckZEW(deck_id):
#     deck = Deck.query.get(deck_id)
#     if not deck:
#         return jsonify({'error': 'Deck not found'}), 404

#     db.session.delete(deck)
#     db.session.commit()
#     return jsonify({'message': 'Deck deleted'}), 200


# @app.route('/add_quiz/<int:deck_id>')
# def add_quiz(deck_id):
#     # Render the page to add a quiz for the given deck_id
#     return render_template('add_quiz.html', deck_id=deck_id)

# @app.route('/add_quiz', methods=['POST'])
# def add_quizz():
#     quiz_id = request.form.get('quiz_id')
#     if quiz_id:
#         # Process the quiz_id and add the quiz
#         return redirect(url_for('home'))  # Redirect back to home page
#     else:
#         # Handle the case where quiz_id is missing
#         return "Please enter a quiz ID"


# @app.route('/quiz', methods=['GET', 'POST'])
# def get_quiz():
#     """ handles quiz on a website """
#     global current_question_index, total_score
#     if request.method == 'GET':
#         return render_template('quiz_2.html', quiz_data=quiz_data)
#     if request.method == 'POST':
#         selected_answer = int(request.form['answer'])
#         if current_question_index < len(quiz_data):
#             current_question = quiz_data[current_question_index]
#             if selected_answer == current_question['correct_answer']:
#                 score = current_question['points']
#                 total_score += score
#             else:
#                 score = 0
#             current_question_index +=1
#             if current_question_index < len(quiz_data):
#                 next_question = quiz_data[current_question_index]
#                 return jsonify({'total_score': total_score, 'current_question_index': current_question_index, 'next_question': next_question})
#             else:
#                 return jsonify({'total_score': total_score, 'current_question_index': current_question_index, 'finished': True})
#         else:
#             return jsonify({'total_score': total_score, 'current_question_index': current_question_index, 'finished': True})
#         # if current_question_index >= len(quiz_data):
#         #     return redirect(url_for('quiz_complete'))

# @app.route('/retake-quiz')
def retake_quiz():
    global current_question_index, total_score
    current_question_index = 0
    total_score = 0
    return render_template('quiz_2.html', quiz_data=quiz_data)
@app.route('/quiz-complete')
def quiz_complete():
    return render_template('quiz_complete.html')

@app.route('/add-question', methods=['POST'])
def add_question():
    # Retrieve form data
    question = request.form.get('new-question')
    answers = []
    
    # Collecting dynamic answers from the form
    for key in request.form:
        if key.startswith('new-answer'):
            answers.append(request.form[key])
    
    # Add the new question to the quiz data
    quiz_data.append({
        'question': question,
        'answers': answers,
        'correct_answer': None,  # You can set this based on user input
        'points': 10  # Default points; you can allow the user to specify this
    })

    # Send a success response
    return jsonify({'success': True, 'message': 'Question added successfully!'})

@app.route('/quiz_management')
def quiz_management():
    return render_template('quiz_management.html')

# @app.route('/save_quiz', methods=['POST'])
# def save_quiz():
#     title = request.form['title']
#     question = request.form['question']
#     option1 = request.form['option1']
#     option2 = request.form['option2']
#     option3 = request.form['option3']
#     correct_answer = request.form['correctAnswer']


#     quiz = Quiz(
#         question = question,
#         option1=option1,
#         option2=option2,
#         option3=option3,
#         correct_answer = correct_answer,
#         title=title
#     )
#     try:
#         db.session.add(quiz)
#         db.session.commit()
#         flash('Quiz saved successfully!', 'success')
#     except:
#         flash('Failed to save quiz.Try again., error')
#     return redirect('quiz_management.html')

# @app.route('/get_quiz')
# def get_quizz():
#     quizzes = Quiz.query.all()
#     quiz_data = []
#     for quiz in quizzes:
#         quiz_data.append({
#             'id': quiz.id,
#             'title': quiz.title,
#             'question': quiz.question,
#             'option1': quiz.option1,
#             'option2': quiz.option2,
#             'option3': quiz.option3,
#             'correct': quiz.correct_answer,
#         })
#     return jsonify(quiz_data)


# @app.route('/delete_quiz/<int:id>', methods=['DELETE'])
# def delete_quiz(id):
#     quiz = Quiz.query.get_or_404(id)
#     try:
#         db.session.delete(quiz)
#         db.session.commit()
#         flash('Quiz deleted successfully!', 'success')
#         return jsonify({'message': 'Quiz deleted successfully'}), 200
#     except:
#         flash('Failed to delete quiz. Try again.', 'error')
#         return jsonify({'error': 'Failed to delete quiz'}), 500 
#     return render_template('quiz_management.html')

# @app.route('/edit_quiz/int:id>', methods=['POST'])
# def edit_quiz(id):
#     quiz = Quiz.query.get_or404(id)
#     quiz.question = request.form['question']
#     quiz.option1 = request.form['option1']
#     quiz.option2 = request.form['option2']
#     quiz.option3 = request.form['option3']
#     quiz.correct_answer = request.form['correctAnswer']
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     try:
#         db.session.commit()
#         flash('Quiz Updated successfully')
#     except:
#         flash('Failed to update quiz. Try again.', 'error')
#     return redirect(url_for('quiz_management'))


if __name__ == '__main__':
    app.run(debug=True)
