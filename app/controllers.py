from app import db, mail #import from __init__ file of app
from flask_mail import Message # for password reset
from app.models import Quiz
from app import mail  # for password reset its flask-mail instance
from flask import current_app as app #proxy to the active Flask application instance.



def get_current_question():
    ''' Retrieves most recent question from database or none if not found '''
    current_question = Quiz.query.order_by(Quiz.id.desc()).first()
    if current_question:
        return current_question
    return None


def send_reset_email(to_email, reset_link):
    ''' sends an email  to user with password reset link
    to_email - email address of user requesting reset
    reset_link - url that user can click to reset password
    '''
    with app.app_context():
        msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[to_email])
        msg.body = f''' To reset your password, Visit link below: {reset_link}
        Password expires after 1 hour. if you did not make this request simply ignore this email'''
        mail.send(msg)
        
        print(f'Send this link to {to_email}: {reset_link}')
