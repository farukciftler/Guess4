CREATE TABLE games (
    room_id VARCHAR(255) NOT NULL PRIMARY KEY,
    generated_number VARCHAR(4) NOT NULL,
    winningturn INT NOT NULL
);

CREATE TABLE guesses (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    guess VARCHAR(4) NOT NULL,
    plus INT NOT NULL,
    minus INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES games(room_id)
);
