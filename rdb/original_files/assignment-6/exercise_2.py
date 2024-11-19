import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return """
    <style>@keyframes colorful {
        0% {color: #f80}
        25% {color: #0f0}
        50% {color: #0ff}
        75% {color: #ff0}
        100% {color: #f80}
    }</style>
    <h1 style="animation:colorful 3s infinite;text-align:center;font-family:Arial">
    🌲🌲🌲Welcome to the Harz Online Shopping Analytics Platform!🌲🌲🌲</h1>"""


# Your solution goes here.

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
