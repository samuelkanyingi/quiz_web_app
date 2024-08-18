document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('quiz-form');
    form.addEventListener('submit', async (events) => {
        events.preventDefault();
        const formData = new FormData(form);
        const selectedAnswer = formData.get('answer')
        if (selectedAnswer == null)
        {
            alert('Please select an answer');
            return;
        }
        const response = await fetch('/quiz', {
            method: 'POST',
            body: new URLSearchParams({answer: selectedAnswer})
        });
        const result = await response.json();
        if (result.finished) {
            document.getElementById('results').innerHTML = `Quiz finished! Your final score is ${result.total_score}. <a href="/retake-quiz">Retake Quiz</a>`;
        }
        else {
            document.getElementById('question').textContent = result.next_question.question;

            // find old answer choices
            const answersContainer = form.querySelectorAll('.answer-option');
            
            // remove old answers
            answersContainer.forEach(option => option.remove());

            // Add new Answer choices
            result.next_question.answers.forEach((answer, index) => {
                const div = document.createElement('div');
                div.className = 'answer-option';

                // add radio button
                const input = document.createElement('input');
                input.type = 'radio';
                input.id = `answer-${index}`;
                input.value = index;
                input.name = 'answer';
                // create label for radio button
                const label = document.createElement('label');
                label.htmlFor = `answer=${index}`;
                label.textContent = answer;
                // add radio button and label to div
                div.appendChild(input)
                div.appendChild(label)
                form.insertBefore(div, form.querySelector('button'));
            });
        }
    });
});