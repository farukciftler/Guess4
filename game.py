from flask import Flask, request, jsonify
import random
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(
    host='localhost',
    port=56241,
    user='root',
    password='sifreyiunutma',
    db='guess_number',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

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

def play(room_id, guess):
    if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
        return jsonify({"error": "Invalid guess. Please enter a 4-digit number with no repeated digits."})
    generated_number = get_generated_number(room_id)
    plus = sum(1 for i, digit in enumerate(guess) if digit == generated_number[i])
    minus = len(set(guess).intersection(generated_number)) - plus
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


if __name__ == "__main__":
    app.run(port=4500)
