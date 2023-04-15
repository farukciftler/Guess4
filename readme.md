# Guess the Number Game

This is a web-based implementation of the "Guess the Number" game, where the player tries to guess a randomly generated 4-digit number with no repeated digits. After each guess, the player is given feedback on how many digits they guessed correctly and how many were in the correct position. The game ends when the player correctly guesses the number.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required packages listed in `requirements.txt`.
3. Start the Flask server by running `python main.py`.
4. Open a web browser and navigate to `http://localhost:4500`.

## API Endpoints

### /getroom [GET]
Generates a new game room with a randomly generated 4-digit number and returns the 5-character room ID.

### /play [POST]
Takes a JSON object with the keys "room_id" and "guess", and returns feedback on the guess in the form of a JSON object with the keys "plus" and "minus". If the guess is correct, the response will include a "message" key with a congratulatory message.

## Technologies Used

- Python 3.8.5
- Flask 1.1.2
- PyMySQL 1.0.2
- Flask-CORS 3.0.10

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
