import os
import sqlite3
from flask import Flask, request, send_from_directory

app = Flask(__name__)


def make_database() -> None:
    conn = sqlite3.connect("tweeter.db")
    cursor = conn.cursor()

    with conn:
        # Delete old tables
        cursor.execute("DROP TABLE IF EXISTS tweet")
        cursor.execute("DROP TABLE IF EXISTS bird")

        # Check foreign key
        cursor.execute("PRAGMA foreign_keys = ON")

        # Create users table.
        # Since "users" is a reserved word in some SQL dialects,
        # we use the thematically more accurate name "bird" instead.
        # Note: Storing plaintext passwords is a bad idea!
        # This is just for the sake of the exercise.
        # In a real application, you should use a key derivation function like Argon2.
        cursor.execute("""
        CREATE TABLE bird (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            verified INTEGER NOT NULL
        )
        """)

        # Create tweet table with username as foreign key
        cursor.execute("""
        CREATE TABLE tweet (
            tweet_username TEXT NOT NULL,
            tweet_text TEXT NOT NULL,
            FOREIGN KEY (tweet_username) REFERENCES bird(username)
        )
        """)

        # Create test birds
        birds = [
            ("bobby", "hunter2", 0),
            ("eltonmollusk", "Do not use this password. Use SQL injection instead.", 1),
            ("Chiquita", "bananas", 1),
            ("ChiquitaBrands", "bananasbananas", 1),
            ("EliLillyandCo", "password", 1),
            ("LillyPad", "95% profit margin", 1),
            ("AzureDiamond", "hunter2", 0),
            ("NestleVerified", "water should not be a human right", 1),
            ("TeslaReal", "who fired the quality control guy?", 1),
            ("News", "this is a fake news account", 1),
        ]
        cursor.executemany("INSERT INTO bird (username, password, verified) VALUES (?, ?, ?)", birds)

        # Create test tweets
        tweets = [
            ("bobby", "Hello, World!"),
            ("eltonmollusk", "Comedy is now legal on Tweeter"),
            ("ChiquitaBrands", "We've just overthrown the government of Brazil!"),
            (
                "Chiquita",
                "We apologize to those who have been served a misleading message from a fake Chiquita account. We have not overthrown a government since 1954.",
            ),
            ("EliLillyandCo", "We are excited to announce insulin is free now."),
            (
                "News",
                "Shares of Eli Lilly dropped 4.2% ($8 billion) after a fake tweeter account named after the company announced that it would be giving away insulin for free.",
            ),
            (
                "LillyPad",
                "We apologyze to those who have been served a misleading message from a fake Lilly account. Our official Tweeter account is @LillyPad.",
            ),
            ("News", "Tesla crashes into child dummy as auto-break test fails"),
            (
                "TeslaReal",
                "Our analysis engineers simulate hundreds of impact scenarios before ever killing a child in real life.",
            ),
            (
                "TeslaReal",
                "Our favorite movie is Total Recall because that's also how car safety regulators refer to our company",
            ),
            (
                "TeslaReal",
                "Honestly the 53% drop in stock price doesn't phase us. if there's anyone who knows about Crashing it's us",
            ),
            ("NestleVerified", "We steal your water and sell it back to you lol"),
            (
                "eltonmollusk",
                'Going forward, any Tweeter handles engaging in impersonation without clearly specifying "parody" will be permanently suspended.',
            ),
        ]
        cursor.executemany("INSERT INTO tweet (tweet_username, tweet_text) VALUES (?, ?)", tweets)


@app.route("/", methods=["GET", "POST"])
def index():
    # Note that SQL injection and XSS are illegal and can land you in jail.
    conn = sqlite3.connect("tweeter.db")

    error_message = ""

    with conn:
        cursor = conn.cursor()

        if request.method == "POST":
            # Add tweet to database
            tweet = request.form["tweet"]
            username = request.form["username"]
            password = request.form["password"]

            # Check password
            cursor.execute(f"SELECT username FROM bird WHERE '{password}' = password AND username = '{username}'")

            rows = cursor.fetchall()

            if len(rows) == 1 and rows[0][0] == username:
                # Add tweet to database
                cursor.execute(
                    "INSERT INTO tweet (tweet_username, tweet_text) VALUES (?, ?)",
                    (username, tweet),
                )
            else:
                error_message = "Incorrect username or password"

        # Get usernames and tweets from database
        cursor.execute("""
        SELECT
            tweet_username,
            tweet_text,
            verified
        FROM
            tweet
            JOIN bird ON tweet.tweet_username = bird.username
        """)

        # Create tweet HTML code
        verified_image = '<img style="height: 1em" src="/static/verified.svg">'
        tweets = "\n".join(f"""
            <div class="tweet">
                <div class="tweet-username">
                    {tweet_username}
                    {verified_image if verified else ''}
                </div>
                <div class="tweet-text">
                {"{}".format(tweet_text)}
                </div>
            </div>
            """ for tweet_username, tweet_text, verified in cursor.fetchall())

    # Assemble website
    return f"""<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Tweeter</title>
        <link rel="stylesheet" href="/static/style.css">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    </head>
<body>
    <div class="container">
        <h1 id="error_message">{error_message}</h1>
        <div class="tweets">{tweets}</div>
        <div class="tweet-form">
            <form action="/" method="POST">
                <table>
                    <!-- for simplicity, the password of the default user is already filled in -->
                    <tr><td>Username</td><td><input type="username" name="username" value="bobby"></td></tr>
                    <tr><td>Password</td><td><input type="password" name="password" value="hunter2"></td></tr>
                    <tr><td></td><td><textarea name="tweet" cols="80" rows="5">I like turtles.</textarea></td></tr>
                    <tr><td></td><td><input id="tweet-button" type="submit" value="Tweet"></td></tr>
                </table>
            </form>
        </div>
    </div>
</body>
</html>
"""


# Serve static files
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    make_database()

    host = os.environ.get("SERVER_HOST", "127.0.0.1")
    host = os.environ.get("SERVER_HOST", "0.0.0.0")
    port = int(os.environ.get("SERVER_PORT", "5000"))

    app.run(host=host, port=port)
