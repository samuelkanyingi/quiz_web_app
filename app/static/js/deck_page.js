// function that toggles visibility of answers
function toggleAnswerVisiblity(iconElement) {
    // Get the answer text element (previous sibling of the eye icon)
    var answerText = iconElement.previousElementSibling;
    console.log(answerText);
    //toggle answer visibility
    if (answerText.style.display === 'none') {
        answerText.style.display = "block"; //show answer
        iconElement.innerHTML = '<i class="fa fa-eye-slash"></i>' // Change icon to "eye-slash"
    }
    else {
        answerText.style.display = 'none';
        iconElement.innerHTML = '<i class="fa fa-eye"></i>' // change to eye
    }
}

// Add quiz modal and button clicked
var addQuizModal = document.getElementById("addQuizModal");
var addQuizBtn = document.getElementById("addQuizBtn");
var closeAddQuizModal = document.getElementById("closeAddQuizModal");
var closeBtn = document.getElementsByClassName("close");

//open add quiz modal when clicked
addQuizBtn.onclick = function() {
   addQuizModal.style.display = "block";
}

//close modal when close (x) is clicked
var closeButtons = document.getElementsByClassName("close");
for (var i = 0; i < closeButtons.length; i++) {
   closeButtons[i].onclick = function() {
       this.parentElement.parentElement.style.display = "none";
   }
}

//reset form when add more quiz is clicked
document.getElementById("addMoreQuizBtn").onclick = function() {
   document.getElementById("addQuizForm").reset();
}

// edit Quiz Modal functionality
var editQuizModal = document.getElementById("editModal");
var closeEditQuizModal = document.getElementById("closeEditModal");

//open edit quiz and populate it with current quiz data
document.querySelectorAll('.edit').forEach(function(button) {
   button.addEventListener('click', function() {
       var quizId = this.getAttribute('data-quiz-id'); // reteive values
       var question = this.getAttribute('data-question');
       var answer = this.getAttribute('data-answer');

       document.getElementById('edit-quiz-id').value = quizId;
       document.getElementById('edit-question').value = question;
       document.getElementById('edit-answer').value = answer;

       editQuizModal.style.display = "block";
   });
});

// close edit quiz modal when close button is clicked
closeBtn.onclick = function() {
   editQuizModal.style.display = "none";
}

// takeQuiz Modal functionality
var takeQuizModal = document.getElementById("takeQuizModal");
var takeQuizBtn = document.getElementById("takeQuizBtn");
var closeTakeQuizModal = document.getElementById("closeTakeQuizModal");

//collect quiz data(questions and answers) from table
function collectQuizData() {
   var quizzes = [];
   var rows = document.querySelectorAll('#quiz-table tbody tr');

   rows.forEach(function(row) {
       //get questions and answers from the table
       var question = row.cells[0].textContent;
       var answer = row.cells[1].textContent;

       quizzes.push({question:question, answer: answer});
   })
   return quizzes;
}
let currentQuestionIndex = 0;
let quizzes = [];

// display current question and answer
function displayCurrentQuestion() {
   var modalContent =  takeQuizModal.querySelector('.modal-content');
   modalContent.innerHTML = ''; // clear previous content

    // Check if there are questions available
    if (quizzes.length === 0) {
       // Display a message or handle the case where no questions are available
       var noQuestionsMessage = document.createElement('p');
       noQuestionsMessage.textContent = 'No questions available.';
       noQuestionsMessage.classList.add('no-questions-message'); // Add CSS class
       modalContent.appendChild(noQuestionsMessage);
       return; // Exit the function if no question
   }

   // create and style progress bar container
   var progressContainer = document.createElement('div')
   progressContainer.classList.add('progress-container'); // add css

   //create and style progress bar itself 
   var progressBar = document.createElement('div')
   progressBar.classList.add('progress-bar') // add css

   // calculate progress as percentage
   var progressPercentage = ((currentQuestionIndex + 1) / quizzes.length) * 100;
   progressBar.style.width = progressPercentage + '%';
   progressBar.textContent = Math.round(progressPercentage) + '%';

   //Append progress bar to container
   progressContainer.appendChild(progressBar);
   modalContent.appendChild(progressContainer)

   // check there are more questions
   if (currentQuestionIndex < quizzes.length) {
       var quiz = quizzes[currentQuestionIndex];

       // create question element
       var questionE1 = document.createElement('p');
       questionE1.textContent = `q${currentQuestionIndex + 1}: ${quiz.question}`;
       questionE1.classList.add('question'); // add CSS class
       questionE1.dataset.questionId = currentQuestionIndex; //set data-question-id
       // Create answer element
       var answerE1 = document.createElement('p');
       answerE1.textContent = `Answer: ${quiz.answer}`;
       answerE1.classList.add('answer'); // add CSS class
       answerE1.style.display = 'none';

       // button to show answer
       var showAnswerBtn = document.createElement('button');
       showAnswerBtn.textContent = 'Show Answer';
       showAnswerBtn.classList.add('show-answer-btn'); // add CSS class
       showAnswerBtn.onclick = function() {
           if(answerE1.style.display === 'block')  {
               answerE1.style.display = 'none';
               showAnswerBtn.textContent = 'Show Answer';
               
           } else {
               answerE1.style.display = 'block';
               showAnswerBtn.textContent = 'Hide Answer';
            
           }
       }
       
         
       // button to move to next question
       var nextQuestionBtn = document.createElement('button');
       nextQuestionBtn.textContent = 'Next Question';
       nextQuestionBtn.classList.add('next-question-btn'); // add CSS class
       nextQuestionBtn.onclick = function() {
           currentQuestionIndex++;
           displayCurrentQuestion();
       };
       modalContent.appendChild(questionE1);
       modalContent.appendChild(showAnswerBtn);
       modalContent.appendChild(answerE1);
       modalContent.appendChild(nextQuestionBtn);

      
   } else {
       // display question when all qustions are answered
       modalContent.innerHTML = '<p><center><h2>Congrats You are finished studying  &#127881 </h2></center> </p>'
       var doneBtn = document.createElement('button');
       doneBtn.textContent = "Done";
       doneBtn.classList.add('done-btn');
       doneBtn.onclick = async function () {
       takeQuizModal.style.display = 'none'; //close modal with done button
    
       }
       var cebrationMessage = document.createElement('celebration')
       cebrationMessage.style.display = 'block';

       setTimeout(function() {
           cebrationMessage.style.display = 'none'
       }, 5000);
       modalContent.appendChild(doneBtn);
       runConfetti();

   }
  
}
// function to trigger confetti animation
function runConfetti() {
   confetti({
       particleCount: 100,
       spread: 70,
       origin: {y : 0.6}
   })
}


takeQuizBtn.onclick = function() {
   quizzes = collectQuizData(); // collect quiz data from table
   currentQuestionIndex = 0;
   displayCurrentQuestion() // display quiz data in a modal
   takeQuizModal.style.display = "block";
}
// Close take quiz modal when close (x) button is clicked
closeTakeQuizModal.onclick = function() {
   takeQuizModal.style.display = "none";
}


// Delete Confirmation Modal references html element
var deleteConfirmationModal = document.getElementById('deleteConfirmationModal');
var closeDeleteModal = document.getElementById("closeDeleteModal");
var confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
var cancelDeleteBtn = document.getElementById("cancelDeleteBtn");

//track quiz item being removed
var quizToDelete = null;

//attach event listeners to delete buttons in the form
document.querySelectorAll('form.inline-delete button[type="submit"]').forEach(function(button) {
   button.addEventListener('click', function(event) {
       //prevent form to submit
       event.preventDefault();
       
       // show confirmation modal
       deleteConfirmationModal.style.display = "block";

       // save current form being submitted
       quizToDelete = event.target.closest('form');
   })
});
// close modal when "no" is clicked
cancelDeleteBtn.onclick = function() {
   deleteConfirmationModal.style.display = "none";
}

//close modal when 'x'  is clicked
closeDeleteModal.onclick = function() {
   deleteConfirmationModal.style.display = "none"
}
// confirm delte action and submit form
confirmDeleteBtn.onclick = function() {
   if(quizToDelete) {
       quizToDelete.submit(); // submit form to delete
   }
   deleteConfirmationModal.style.display = "none";
};



function loadNextQuestion() {
   fetch('/get_next_question')
   .then(response => response.json())// Ensures the server is returning JSON
   .then(data => {
       if (data.question) {
           console.log('Next question:', data.question);
           document.querySelector('#takeQuizModal .question').textContent = data.question;
           document.querySelector('#takeQuizModal .answer').textContent = `Answer: ${data.answer}`;
       } else {
           console.log('Next question:', data.question)
           document.querySelector('#takeQuizModal p').textContent = data.question;
       }
   })
   .catch(error => {
           console.error('Error fetching next question:', error);
       });
}


// Handle clicks outside of modals
window.onclick = function(event) {
   if (event.target == addQuizModal) {
       addQuizModal.style.display = "none";
   } else if (event.target == editQuizModal) {
       editQuizModal.style.display = 'none';
   } else if (event.target == takeQuizModal) {
       takeQuizModal.style.display = "none";
   }
   else if (event.target == deleteConfirmationModal) {
       deleteConfirmationModal.style.display = "none";
   }
};