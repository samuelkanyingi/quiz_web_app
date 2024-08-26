from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from app.models import Deck, Quiz
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def landing_page():
    return render_template('landing_page.html')

@user_bp.route('/home')
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

