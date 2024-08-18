function editDeck(deckId) {
    // Implement edit deck functionality
    console.log('Edit deck:', deckId);
}
function deleteDeck(id, row) {
    // Implement delete deck functionality
    console.log('Delete deck:', id);
    fetch(`/delete_deck/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          row.remove(); // Remove row from table
        } else {
          console.error(data.error);
        }
      })
      .catch(error => {
        console.error("Error while deleting", error);
      });
    }


    let deckId;
    let editIndex;

    // Function to show Add popup
    function showAddPopup() {
        document.getElementById("myPopup").style.display = 'block';
    }

    // Function to show Edit popup
    function showEditPopup(index) {
        const deckNameElement = document.getElementById(`deck-name-${index}`);
        if (deckNameElement) {
            document.getElementById("edit-deck-name-input").value = deckNameElement.textContent;
        } else {
            document.getElementById("edit-deck-name-input").value = '';
        }
        document.getElementById("editPopup").style.display = "block";
        editIndex = index;
    }

    // Function to close popups
    function closePopup(popupId) {
        document.getElementById("deck-name-input").value = '';
        document.getElementById(popupId).style.display = 'none';
    }

    // Function to add deck dynamically
    function addDeck() {
        const deckName = document.getElementById("deck-name-input").value;
        closePopup('myPopup');
        const quizCount = 0;

        fetch('/add_deck', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: deckName,
                quiz_count: quizCount
            })
        })
        .then(response => response.json())
        .then(data => {
            window.deckId = data.id;
            const table = document.getElementById('quiz-table').getElementsByTagName('tbody')[0];
            const row = table.insertRow();
            row.setAttribute("id", `row-${data.id}`);
            row.setAttribute("data-deck-id", data.id);

             // Create a hyperlink for the deck name that redirects to the add quiz page
            const deckLink = document.createElement('a');
            deckLink.href = `/add_quiz/${data.id}`; // Link to add quizzes for this deck
            deckLink.textContent = deckName; // Display the deck name as the clickable link
            
            // cell1.appendChild(deckLink);

            const cell1 = row.insertCell(0);
            cell1.appendChild(deckLink);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);

            // cell1.textContent = deckName;
            cell2.textContent = quizCount;

            // Add an edit button
            const editButton = document.createElement('button');
            editButton.textContent = 'Edit';
            editButton.onclick = () => showEditPopup(table.rows.length - 1);
            cell3.appendChild(editButton);

            // Add space between buttons
            cell3.appendChild(document.createTextNode(" "));

            // Add delete button
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            //deleteButton.onclick = () => deleteDeck(data.id, row);
            deleteButton.onclick = () => deleteDeck(row.getAttribute("data-deck-id"), row);

            cell3.appendChild(deleteButton);
            
            adjustContainerHeight();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to save edited deck
    function saveEditedDeck() {
        const deckNameElement = document.getElementById(`deck-name-${editIndex}`);
        if (deckNameElement) {
            deckNameElement.textContent = document.getElementById("edit-deck-name-input").value;
        }
        closePopup('editPopup');
    }

    // Function to adjust container height
    function adjustContainerHeight() {
        const container = document.getElementById('table-container');
        const table = document.getElementById('quiz-table');
        container.style.maxHeight = table.offsetHeight + 'px';
    }

    // Function to delete a deck
    function deleteDeck(id, row) {
        fetch(`/delete_deck/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            window.deckId = data.id;
            if (data.message) {
                row.remove(); // Remove row from table
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error("Error while deleting", error);
        });
    }

    // Function to fetch decks on load
    function getDecks() {
        fetch('/get_decks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('quiz-table').getElementsByTagName('tbody')[0];
            data.forEach(deck => {
                const row = table.insertRow();
                row.setAttribute("id", `row-${deck.id}`);

                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                const cell3 = row.insertCell(2);

                cell1.textContent = deck.name;
                cell2.textContent = deck.quiz_count;

                // Add edit button
                const editButton = document.createElement('button');
                editButton.textContent = 'Edit';
                editButton.onclick = () => showEditPopup(table.rows.length - 1);
                cell3.appendChild(editButton);

                adjustContainerHeight();
            });
        })
        .catch(error => {
            console.error('Error retrieving decks:', error);
        });
    }

    window.addEventListener('load', getDecks);