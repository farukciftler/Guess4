from flask import Flask, request, jsonify
import random
import pymysql.cursors
import string
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

connection = pymysql.connect(
    host='localhost',
    port=49703,
    user='root',
    password='sifreyiunutma',
    db='guess_number',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def generate_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_number():
    while True:
        first_digit = random.randint(1, 9)
        last_three_digits = random.randint(0, 999)
        number = str(first_digit) + str(last_three_digits).zfill(3)
        if len(set(number)) == 4:
            return number


def get_generated_number(room_id):
    with connection.cursor() as cursor:
        sql = "SELECT generated_number FROM games WHERE room_id = %s"
        cursor.execute(sql, (room_id,))
        result = cursor.fetchone()
        if result is None:
            generated_number = generate_number()
            sql = "INSERT INTO games (room_id, generated_number, winningturn) VALUES (%s, %s,0)"
            cursor.execute(sql, (room_id, generated_number))
            connection.commit()
        else:
            generated_number = result["generated_number"]
        return generated_number
    
def count_identical_digits(num1, num2):
    # Convert the numbers to strings and split them into lists of digits
    digits1 = list(str(num1))
    digits2 = list(str(num2))

    # Initialize a variable to store the count of identical digits
    count = 0

    # Iterate through the digits of the first number
    for digit1 in digits1:
        # Check if the digit is in the second number and is not in the same position
        if digit1 in digits2 and digits2.index(digit1) != digits1.index(digit1):
            # If the digit is found in the second number and is not in the same position,
            # increment the count variable
            count += 1
            # Remove the digit from the second number to avoid counting it twice
            digits2.remove(digit1)
    
    # Return the count of identical digits
    return count


def play(room_id, guess):
    if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
        return jsonify({"error": "Invalid guess. Please enter a 4-digit number with no repeated digits."})
    generated_number = get_generated_number(room_id)
    plus = sum(1 for i, digit in enumerate(guess)
               if digit == generated_number[i])
    minus = count_identical_digits(guess,generated_number)
    if plus == 4:
        with connection.cursor() as cursor:
            sql = "INSERT INTO guesses (room_id, guess, plus, minus) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (room_id, guess, plus, minus))
            connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) AS total_guesses FROM guesses WHERE room_id = %s"
            cursor.execute(sql, (room_id,))
            total_guesses = cursor.fetchone()["total_guesses"]
            sql = "UPDATE games SET winningturn = %s WHERE room_id = %s"
            cursor.execute(sql, (total_guesses, room_id))
            connection.commit()
        
        return jsonify({"message": "Congratulations, you guessed the number!"})
    else:
        with connection.cursor() as cursor:
            sql = "INSERT INTO guesses (room_id, guess, plus, minus) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (room_id, guess, plus, minus))
            connection.commit()
        return jsonify({"plus": plus, "minus": minus})


@app.route("/play", methods=["POST"])
def play_endpoint():
    data = request.get_json()
    room_id = data.get("room_id")
    guess = data.get("guess")
    return play(room_id, guess)


@app.route("/getroom", methods=["GET"])
def getroom():
    try:
        with connection.cursor() as cursor:
            generated_number = generate_number()
            room_id = generate_random_string(5)
            sql = "INSERT INTO games (room_id, generated_number, winningturn) VALUES (%s, %s,0)"
            cursor.execute(sql, (room_id, generated_number))
            connection.commit()
            return jsonify({"room_id": room_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=4500)
