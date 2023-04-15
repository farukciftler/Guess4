# Guess the Number Game

This is a web-based implementation of the "Guess the Number" game, where the player tries to guess a randomly generated 4-digit number with no repeated digits. After each guess, the player is given feedback on how many digits they guessed correctly and how many were in the correct position. The game ends when the player correctly guesses the number.

## Getting Started

To run this game locally, you need to have Python 3, Flask, PyMySQL, and Flask-CORS installed. You also need to have a MySQL server running.

1. Clone this repository
2. Install the required packages using `pip install -r requirements.txt`
3. Update the database connection information in `app.py` to match your MySQL server configuration
4. Run `app.py` using `python app.py`
5. Visit http://localhost:4500 in your web browser to play the game

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


### Endpoints

#### `/getroom` [GET]

This endpoint generates a new game room and returns the room ID.

**Request Parameters:**

None.

**Response:**

- `room_id` (string): The ID of the newly generated game room.

#### `/play` [POST]

This endpoint is used to play the game by making a guess.

**Request Parameters:**

- `room_id` (string): The ID of the game room.
- `guess` (string): A 4-digit number with no repeated digits.

**Response:**

If the guess is valid:

- If the guess is correct:
    - `message` (string): A congratulations message.
- If the guess is incorrect:
    - `plus` (int): The number of digits in the correct position.
    - `minus` (int): The number of digits in the wrong position.

If the guess is invalid:

- `error` (string): An error message describing the issue with the guess.


# Guess the Number Game Database

The Guess the Number game uses a MySQL database to store the generated number and the guesses made by the players. The database has two tables:

1. **games** table: stores the game information including the room_id, generated_number, and winningturn.

| Column Name      | Data Type | Description                               |
|------------------|-----------|--------------------------------------------|
| room_id            | varchar(5) | The room ID of the game.                       |
| generated_number | varchar(4) | The randomly generated 4-digit number. |
| winningturn       | int           | The number of turns taken to guess the number. |

2. **guesses** table: stores the guesses made by the players.

| Column Name      | Data Type | Description                                       |
|------------------|-----------|----------------------------------------------------|
| id                    | int           | The unique ID of the guess.                                  |
| room_id            | varchar(5) | The room ID of the game.                                        |
| guess               | varchar(4) | The 4-digit number guessed by the player.          |
| plus                 | int           | The number of digits in the correct position.        |
| minus              | int           | The number of digits in the wrong position.      |



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
