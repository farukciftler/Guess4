const API_URL = "http://localhost:4500";

const digits = document.querySelectorAll(".number-row input");
const submitButton = document.querySelector("#submit-button");
const resetButton = document.querySelector("#reset-button");
const plusElement = document.querySelector("#plus");
const minusElement = document.querySelector("#minus");
const messageBox = document.querySelector(".message-box");

let roomID = null;

// Helper function to reset the game board
function resetBoard() {
	plusElement.textContent = "";
	minusElement.textContent = "";
	messageBox.innerHTML = "";
	submitButton.disabled = false;
	document.querySelector("#number-input").value = "";

	resetButton.addEventListener("click", resetBoard);

	// Initialize the game by requesting a new room ID from the server
	fetch(API_URL + '/getroom', {
			method: "GET"
		})
		.then((response) => response.json())
		.then((data) => {
			roomID = data.room_id;
			showMessage(`Room ID: ${roomID}`);
		})
		.catch(() => showMessage("Failed to connect to the server", true));
}

// Helper function to display a message in the message box
function showMessage(message, isError = false) {
	messageBox.innerHTML = message;
	messageBox.style.color = isError ? "red" : "green";
}

// Helper function to add a guess to the guesses list
function addGuessToList(guess, plus, minus) {
    const guessesList = document.querySelector("#guesses-list");
    const guessItem = document.createElement("li");
    guessItem.innerHTML = `${guess} <span class="plus-minus">( ${plus} + ${minus} )</span>`;
    guessesList.appendChild(guessItem);
}

// ...

async function sendGuess(guess) {
    const response = await fetch(API_URL + '/play', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            room_id: roomID,
            guess
        }),
    });
    const data = await response.json();
    if (data.error) {
        showMessage(data.error, true);
    } else if (data.message) {
        showMessage(data.message);
        submitButton.disabled = true;
    } else {
        plusElement.textContent = data.plus;
        minusElement.textContent = data.minus;
        addGuessToList(guess, data.plus, data.minus);
    }
}



// Event listeners for the buttons
submitButton.addEventListener("click", () => {
	const guess = document.querySelector("#number-input").value;
	sendGuess(guess);
});

resetButton.addEventListener("click", resetBoard);

// Initialize the game by requesting a new room ID from the server
fetch(API_URL + '/getroom', {
		method: "GET"
	})
	.then((response) => response.json())
	.then((data) => {
		roomID = data.room_id;
		showMessage(`Room ID: ${roomID}`);
	})
	.catch(() => showMessage("Failed to connect to the server", true));