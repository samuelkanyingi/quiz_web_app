# FlashCard app

A web based application that allows users to create, manage and take quizzes. The application include features sucha s user authentication, deck creation, editing and deleteion. Inside decks you can add, edit and delete questions and answers and finally take quiz from the questions and answers populated.

## Table of Contents

* Project Overview 
* Architecture Overview
* Setup Instructions
* Usage GuideLines
* Features
* Contributing
* License

## Project Overview 
This project is a flashcard application built using flask on the backend and html, css and javascript on the frontend. It allows users to create decks that store quizzez, add questions and manage questions and finally take quiz.

# Architucture Overview
Our app uses microservice architecture for frontend and backend

### Backend
* Flask: A web framework built on python used to handle HTTP request and manage user sessions.
* Flask-SQLAlchemy: libary used  for database interations with MySQL.
* MySQL: The dtabse used for storing decks, user details, question and answers

### Frontend
* HTML - used to render user interface
* css - used to style user interface
* javascript - used to add interactivity and dynamic capabilities


## SetUp Instructions
### Prerequisites
* **Python 3.5+**: Make sure python is installed locally
* **MySQL**: Ensure MySql is installed and running

## Backend Setup
**1. Clone the repository**
```
Clone the repo http://github.com/samuelkanyingi/quiz_web_app.git
cd quiz-web_app
```

**2. Install Python dependencies**
```
pip install -r requirements.txt
```

**3.  Initialize the database** 
```
flask db init
flask db migrate
flask db upgrade
``` 

**4. Run the Flask Server**
```
flask run
```

## Usage Guidelines
### Running the applcation
* **Start with backend**: Ensure Flask Server is running

### Create a quiz
1. Log in your account
2. Click Add Deck button
3. Click deck name and navigate to add new question button
5. Add question and answers and click save button
6. Click take quiz button to start quiz

### Managing Quizzes
* **Edit** - navigate your deck rows and select 'Edit' to modify quiz details.
* **Delete** - Use Delete button to remove questions or entire deck

## Features
* User Authentication: Secure login and registration
* Deck creation
* Question and answer management
quiz taking

## Contributing
* Please Submit a pull request to add a new feature
* Open an issue  for improvements

## License
This project is licensed under the MIT license


