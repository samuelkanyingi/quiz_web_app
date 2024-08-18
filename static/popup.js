document.addEventListener('DOMContentLoaded', () => {
    const addQuestionBtn = document.getElementById('add-question-btn');
    const popupFormContainer = document.getElementById('popup-form-container');
    const closePopup = document.getElementById('close-popup');
    const addAnswerOptionBtn = document.getElementById('add-answer-option');
    const answerOptionsContainer = document.getElementById('answer-options');
    let answerCount = 1;

    // Show the pop-up form
    addQuestionBtn.addEventListener('click', () => {
        popupFormContainer.classList.remove('popup-hidden');
    });

    // Hide the pop-up form
    closePopup.addEventListener('click', () => {
        popupFormContainer.classList.add('popup-hidden');
    });

    // Add more answer options dynamically
    addAnswerOptionBtn.addEventListener('click', () => {
        const newAnswerLabel = document.createElement('label');
        newAnswerLabel.setAttribute('for', `new-answer-${answerCount}`);
        newAnswerLabel.textContent = `Answer Option ${answerCount + 1}:`;

        const newAnswerInput = document.createElement('input');
        newAnswerInput.setAttribute('type', 'text');
        newAnswerInput.setAttribute('id', `new-answer-${answerCount}`);
        newAnswerInput.setAttribute('name', `new-answer-${answerCount}`);
        newAnswerInput.setAttribute('required', true);

        answerOptionsContainer.appendChild(newAnswerLabel);
        answerOptionsContainer.appendChild(newAnswerInput);

        answerCount++;
    });
});
