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


# You can remove the route above if you want to.

# Your solution goes here.

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
