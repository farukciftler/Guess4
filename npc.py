import requests
import json
import random
import string

BASE_URL = "http://localhost:4500/play"

def play_game(room_id):
    print("Starting game with room ID:", room_id)
    possible_solutions = generate_possible_solutions()
    while True:
        guess = random.choice(possible_solutions)
        data = {"room_id": room_id, "guess": guess}
        response = requests.post(BASE_URL, json=data)
        result = json.loads(response.text)
        if "error" in result:
            print("Invalid guess:", guess)
            possible_solutions.remove(guess)
        elif "message" in result:
            print("Congratulations, you won with guess:", guess)
            break
        else:
            print("Guess:", guess, "Plus:", result["plus"], "Minus:", result["minus"])
            possible_solutions = filter_solutions(possible_solutions, guess, result)

def generate_possible_solutions():
    return [str(i).zfill(4) for i in range(10000) if len(set(str(i))) == 4]

def filter_solutions(possible_solutions, guess, result):
    plus = result["plus"]
    minus = result["minus"]
    filtered_solutions = []
    for solution in possible_solutions:
        solution_plus = sum(1 for i, digit in enumerate(guess) if digit == solution[i])
        solution_minus = len(set(guess).intersection(solution)) - solution_plus
        if solution_plus == plus and solution_minus == minus:
            filtered_solutions.append(solution)
    return filtered_solutions

def random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

if __name__ == "__main__":
    while True:
        room_id = random_string(10)
        play_game(room_id)
