from flask import Blueprint, request, redirect, url_for, jsonify
from app.models import Quiz, db
from datetime import datetime, timedelta
from app.controllers import get_current_question

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/add_quiz', methods=['POST'])
def add_quiz():
    ''' adds new question and answer in deck_page.html '''
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
        return redirect(url_for('deck.deck_page', deck_id=deck_id))
    else:
        return "Error: missing form data"

@quiz_bp.route('/edit_quiz', methods=['POST'])
def edit_quiz():
    ''' edits a question and answer in deck_page.html'''
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
    return redirect(url_for('deck.deck_page', deck_id=quiz.deck_id))

@quiz_bp.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    ''' Post request to delete quiz in deck_page.html'''
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('deck.deck_page', deck_id=quiz.deck_id))


@quiz_bp.route('/get_current_question_id', methods=['GET'])
def get_current_question_id():
    '''
    returns id of current question 
    used when by edit question modal popup in deck_page.html
    '''
    current_question = get_current_question()  # method to fetch the current question
    if current_question:
        return jsonify({'id': current_question.id})
    else:
        return jsonify({'error': 'No current question found'}), 404


@quiz_bp.route('/get_next_question', methods=['GET'])
def get_next_question():
    ''' retrieves next question '''
    global current_question_index #keeps track of current question
    print(f"Current question index: {current_question_index}") # debugging line
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


