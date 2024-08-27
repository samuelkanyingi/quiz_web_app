from flask import Blueprint, request, redirect, url_for, jsonify, flash, render_template
from flask_login import login_required, current_user
from app.models import Deck, Quiz, db
from datetime import datetime, timedelta


deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/add_deck', methods=['POST'])
@login_required
def add_deck():
    ''' adds new deck in home.html'''
    if request.method == 'POST':
        print("Received POST request for adding a deck")
        title = request.form['title']
        print(f"Received title: {title}")
        # Create a new deck object
        new_deck = Deck(title=title, name='Default Name', quiz_count=0, user_id=current_user.id)
        db.session.add(new_deck)
        db.session.commit()
    
        flash('Deck created successfully!!!', 'success')
        return redirect(url_for('user.home'))
    else:
        return render_template('home.html')

@deck_bp.route('/edit_deck', methods=['POST'])
def edit_deck():
    ''' updates deck in home.html '''
    # Retrieve deck ID and new title from the form data
    deck_id = request.form.get('deck_id')
    new_title = request.form.get('title')

    if deck_id and new_title:
        # Query the deck from the database using the deck_id
        deck = Deck.query.get(deck_id)
        if deck:
            deck.title = new_title
            db.session.commit()
            flash('Deck updated successfully!!!!', 'success')
    return redirect(url_for('user.home'))


@deck_bp.route('/delete_deck/<int:deck_id>', methods=['POST', 'DELETE'])
def delete_deck(deck_id):
    ''' deletes deck and return json response to home.js file '''
    deck_to_delete = Deck.query.get_or_404(deck_id)
    db.session.delete(deck_to_delete)
    db.session.commit()

    return jsonify({'success': True}), 200 

@deck_bp.route('/deck/<int:deck_id>', methods=['GET'])
def deck_page(deck_id):
    ''' upon GET request it returns deck_page.html '''
    deck = Deck.query.get_or_404(deck_id) 
    quizzes = Quiz.query.filter_by(deck_id=deck_id).all()    
    return render_template('deck_page.html', deck=deck, quizzes=quizzes)

