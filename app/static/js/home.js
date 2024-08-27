//wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function(){
    //select all flash messages
    const flashMessages = document.querySelectorAll('.flash');
    //set timeout for flash messae to fade out after delay
    flashMessages.forEach(function(flash){
        setTimeout(function() {
            flash.style.transition = 'opacity 0.5s ease-out' //fade-out effect
            flash.style.opacity = "0"; //start fadeout
            setTimeout(function() {
                flash.remove(); // remove element from DOM
            }, 500); // wait for fadeout
        }, 2000) //start faceout after 2 seconds
    })
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modals = document.getElementById('delete-modal')
    const confirmDeleteButton = document.getElementById('confirm-delete-btn')
    const cancelDeleteButton = document.getElementById('cancel-delete-btn')
    
    let deckIdToDelete = null; // Variable to store the ID of the deck to delete
    //open delete modal when delete button is clicked
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('Clicked button:', this); // Log the button element
            deckIdToDelete = this.getAttribute('data-deck-id'); // Get the deck ID from the clicked button
            console.log('Deck ID to delete:', deckIdToDelete); // Log the deck ID
            modals.style.display = "block"; // show modal
        });
    })
    // close modal when No is clicked
    cancelDeleteButton.addEventListener('click', function() {
        modals.style.display = 'none'; //hide modal
    })
    //handle delection action when confirm button is clicked
    confirmDeleteButton.addEventListener('click', function() {
        console.log('Confirm delete clicked for Deck ID:', deckIdToDelete); // Log confirmation
        if (deckIdToDelete) {
            deleteDeck(deckIdToDelete) //call deleteDeck to delete
            modals.style.display = 'none'; //hide delete modal
        }
    })
    // function to show flash message
    function showFlashMessage(message, type) {
        const flashContainer = document.getElementById('flash-messages');
        if (!flashContainer) {
            location.reload(); //reload if flash container is not found
            
        }
        //create a flash element
        const flashMessage  = document.createElement('div'); 
            flashMessage.className = `flash flash-${type}`; // add class based om message type
            flashMessage.textContent = message; // set flah message text
            flashContainer.appendChild(flashMessage) //append flash message
            
            setTimeout(() => {
                flashMessage.style.transition.opacity = '0' // start fadeout
                setTimeout(()=> flashMessage.remove(), 500) // remove flah message after fade out
            }, 1000) // start fadeout after 1 second
        }
        
    
    //function to delete deck
    function deleteDeck(deckId) {
        //make API Call to server
        console.log('Deleting Deck ID:', deckId);
        fetch(`/delete_deck/${deckId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('deck deleted')
                showFlashMessage('Deck deleted successfully', 'success')
                
                //remove element from dom
            }
            else {
                showFlashMessage('Failed to delete deck', 'error')
            }
        })
        .catch(error => console.error('Error:', error))
    }
})
function addCloseButtonListeners() {
    var closeButtons = document.querySelectorAll('.flash-message .close')
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function(){
            var flashMessage = button.parentElement;
            flashMessage.style.display = 'none';
        });
    });
}
    var modal = document.getElementById("myModal")
    var btn = document.getElementById("myBtn")
    var span = document.querySelector(".close-add-deck")
    btn.onclick = function() {
        modal.style.display = "block";
    }
    span.onclick = function() {
        modal.style.display = "none";
    }


// Functionality for Edit Deck Modal
var editModal = document.getElementById("editModal");
var closeEditModal = editModal.getElementsByClassName("close")[0];

document.querySelectorAll('.edit-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var deckId = this.getAttribute('data-deck-id');
        var deckTitle = this.getAttribute('data-deck-title');
        //populate modal form with selected deck data
        document.getElementById('edit-deck-id').value = deckId;
        document.getElementById('edit-deck-title').value = deckTitle;
        editModal.style.display = "block"; // show edit modal
    });
});
//close edit modal
closeEditModal.onclick = function() {
    editModal.style.display = "none";
}
document.addEventListener('DOMContentLoaded', function() {
    var logoutBtn = document.getElementById('logoutBtn');
    var logoutModal = document.getElementById('logoutModal');
    var closeLogoutModal = document.getElementsByClassName('close')[0];
    var confirmLogoutBtn = document.getElementById('confirmLogout');
    var cancelLogoutBtn = document.getElementById('cancelLogout')
    
    //show modal when button clicked
    logoutBtn.onclick = function() {
        logoutModal.style.display = 'block';
    }
    //close modal when x is clicked
    closeLogoutModal.onclick = function() {
        logoutModal.style.display = 'none';
    }
    //close modal when no is clicked
    cancelLogoutBtn.onclick = function() {
        logoutModal.style.display = "none";
    }
    // logout when yes is clicked
    confirmLogoutBtn.onclick = function() {
        logoutModal.style.display = "none";
        window.location.href = '/logout'
    }
})
window.onclick = function(event) {
    if (event.target == editModal) {
        editModal.style.display = "none";
        
    }
}