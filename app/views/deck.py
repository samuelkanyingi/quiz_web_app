from flask import Blueprint, request, redirect, url_for, jsonify, flash, render_template
from flask_login import login_required, current_user
from app.models import Deck, Quiz, db
from datetime import datetime, timedelta


deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/add_deck', methods=['POST'])
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
        return redirect(url_for('user.home'))
    else:
        return render_template('home.html')

@deck_bp.route('/edit_deck', methods=['POST'])
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
    return redirect(url_for('user.home'))


@deck_bp.route('/delete_deck/<int:deck_id>', methods=['POST', 'DELETE'])
def delete_deck(deck_id):
    deck_to_delete = Deck.query.get_or_404(deck_id)
    db.session.delete(deck_to_delete)
    db.session.commit()

    return jsonify({'success': True}), 200

@deck_bp.route('/deck/<int:deck_id>', methods=['GET'])
def deck_page(deck_id):
    deck = Deck.query.get_or_404(deck_id) 
    quizzes = Quiz.query.filter_by(deck_id=deck_id).all()    
    return render_template('deck_page.html', deck=deck, quizzes=quizzes)

@deck_bp.route('/decks')
def get_decks():
    decks = Deck.query.all()
    return render_template('home.html', decks=decks)

@deck_bp.route('/get_decks')
def get_deck():
    decks = Deck.query.all()
    decks_list = [deck.to_dict() for deck in decks]
    return jsonify(decks_list), 200

@deck_bp.route('/decks', methods=['POST'])
def create_deck():
    data = request.get_json()
    new_deck = Deck(name=data['name'], quiz_count=data['quiz_count'])
    db.session.add(new_deck)
    db.session.commit()
    return jsonify(new_deck.to_dict()), 201

@deck_bp.route('/deck/<int:deck_id>', methods=['PUT'])
def update_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({'error': 'Deck not found'}), 404

    data = request.get_json()
    deck.name = data['name']
    deck.quiz_count = data['quiz_count']
    db.session.commit()
    return jsonify(deck.to_dict())
