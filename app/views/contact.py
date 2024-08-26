from flask import Blueprint, request, render_template
from app.models import User
from flask_mail import Message

#instance of blueprint class
contact_bp = Blueprint('contact', __name__) #name of bluprint and current module

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    ''' Handles http requests to contact routes
    '''
    if request.method == 'POST':
        #extract form data values
        subject = request.form['subject']
        email = request.form['email']
        message = request.form['message']

        #create an email message
        msg = Message(subject, sender=email,
                      recipients=['samuelkanyingi2016@gmail.com']) #Message class used to create an email message
        msg.body = f'Message from {email}\n\n {message}'

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash('Message  failed to send.Please try again later.', 'error')
            return redirect(url_for('contact'))
    return render_template('contact.html') #GET Request
