from flask import Flask, request
import html
import psycopg

app = Flask(__name__)

users = [
    {"username": "Spiderman", "firstname": "Peter", "lastname": "Parker"},
    {"username": "Green Goblin", "firstname": "Norman", "lastname": "Osborn"},
    {"username": "Mary", "firstname": "Mary Jane", "lastname": "Watson"},
    {"username": "Harry", "firstname": "Harry", "lastname": "Osborn"},
    {"username": "May", "firstname": "May", "lastname": "Parker"},
    {"username": "Ben", "firstname": "Ben", "lastname": "Parker"},
]

users_dict = {user["username"]: user for user in users}


@app.route("/python", methods=["GET", "POST"])
def hello_from_python() -> str:
    message = "Hello from Python! Please log in!"

    if "username" in request.form:
        username = request.form["username"]

        if username in users_dict:
            user = users_dict[username]

            message = f'Hello, {user["firstname"]} {user["lastname"]}!'

    website = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Hello!</title></head>
<body>
    <h1>{html.escape(message)}</h>
    <form action="/python" method="post">
        <input name="username" type="text" value="Spiderman">
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""
    return website


# Your solution goes here.

connection = psycopg.connect()
cursor = connection.cursor()
# Create a table for the users
cursor.execute(
"""
CREATE TABLE
    users
(
    username TEXT PRIMARY KEY NOT NULL,
    firstname TEXT,
    lastname TEXT
)
"""
)

# Insert data into database
users_insert = [tuple(user.values()) for user in users]

cursor.executemany("""
                INSERT INTO
                    users (username, firstname, lastname)
                VALUES
                    (%s, %s, %s)
            """, users_insert)

connection.commit()


@app.route("/sql", methods=["GET", "POST"])
def hello_from_sql() -> str:


    # Start the webpage construction
    message = "Hello from SQL! Please log in!"

    if "username" in request.form:
        username = request.form["username"]
        print("ok")
        cursor.execute("""
                        SELECT
                            firstname, lastname
                        FROM
                            users
                        WHERE
                            username = (%s)
        """, (username,))

        user = cursor.fetchone()
        if user is not None:
            message = f'Hello, {user[0]} {user[1]}!'
        else:
            message = f'{username}, do you even know Parker?'



    website = f"""<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>Hello!</title></head>
    <body>
        <h1>{html.escape(message)}</h1>
        <form action="/sql" method="post">
            <input name="username" type="text" value="Spiderman">
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """

    return website


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
