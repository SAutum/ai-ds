import urllib.request
import urllib.parse
import subprocess
import threading
import traceback
import secrets
import psycopg
import atexit
import typing
import signal
import socket
import zipme
import time
import sys
import os


def check_database_connection() -> None:
    try:
        conn = psycopg.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
    except psycopg.OperationalError:
        traceback.print_exc()
        print(
            "Did you start a PostgreSQL database and set the environment variables PGUSER, PGHOST and PGPASSWORD correctly?"
        )
        for name in ["PGUSER", "PGHOST", "PGPASSWORD"]:
            print("The value for", name, "is", repr(os.environ.get(name)))
        sys.exit(1)


def spawn_server(command: list[str], host: str, port: int, timeout: float = 2.0) -> None:
    # Check if no server is started yet
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        if 0 == sock.connect_ex((host, port)):
            print(f"Port {port} already in use. Please stop whatever is using this port and try again.")
            sys.exit(1)

    # Start server as a new process
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    )

    # Make server process kill itself when main process dies
    def kill() -> None:
        process.send_signal(signal.SIGTERM)
        # Wait for process to die a graceful death
        process.wait()

    atexit.register(kill)

    # Forward stdout and stderr from server process to main process
    for pipe in [process.stdout, process.stderr]:

        def print_pipe(std: typing.TextIO) -> None:
            for line in iter(pipe.readline, ""):
                if line.endswith("\n"):
                    line = line[:-1]
                print(line)

        thread = threading.Thread(target=print_pipe, args=(pipe,))
        thread.daemon = True
        thread.start()

    # Wait for one second or until server is reachable
    start_time = time.perf_counter()

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if 0 == sock.connect_ex((host, port)):
                return

        elapsed_time = time.perf_counter() - start_time

        if elapsed_time > timeout:
            raise TimeoutError(
                f"After waiting for {timeout} seconds, the server at {host}:{port} was still unreachable"
            )

        time.sleep(0.01)


def test() -> None:
    users = [
        {"username": "Spiderman", "firstname": "Peter", "lastname": "Parker"},
        {"username": "Green Goblin", "firstname": "Norman", "lastname": "Osborn"},
        {"username": "Mary", "firstname": "Mary Jane", "lastname": "Watson"},
        {"username": "Harry", "firstname": "Harry", "lastname": "Osborn"},
        {"username": "May", "firstname": "May", "lastname": "Parker"},
        {"username": "Ben", "firstname": "Ben", "lastname": "Parker"},
    ]

    check_database_connection()

    # Cleanup
    with psycopg.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS users")

    host = "127.0.0.1"
    port = 5000

    spawn_server([sys.executable, "exercise_2_a.py"], host, port)

    # Modify firstnames and lastnames
    with psycopg.connect() as conn:
        for user in users:
            user["firstname"] += "_" + secrets.token_hex(4)
            user["lastname"] += "_" + secrets.token_hex(4)

            query = "UPDATE users SET firstname = %(firstname)s, lastname = %(lastname)s WHERE username = %(username)s"

            conn.execute(query, user)

    url = f"http://{host}:{port}/sql"

    with urllib.request.urlopen(url, timeout=2) as r:
        response = r.read().decode("utf-8")

    assert "Hello" in response, f'Response did not contain the word "Hello":\n\n{response}\n'
    assert "Harry" not in response, f'Response should not contain the word "Harry":\n\n{response}\n'

    # Check if text is on website
    for user in users:
        username = user["username"]
        firstname = user["firstname"]
        lastname = user["lastname"]

        data = urllib.parse.urlencode({"username": username}).encode("utf-8")

        request = urllib.request.Request(url, data=data)

        with urllib.request.urlopen(request, timeout=2) as r:
            response = r.read().decode("utf-8")

        assert firstname in response, f'Website did not contain the text "{firstname}":\n\n{response}\n'
        assert lastname in response, f'Website did not contain the text "{lastname}":\n\n{response}\n'

        if username != "Harry":
            assert "Harry" not in response, f'Response should not contain the word "Harry":\n\n{response}\n'


if __name__ == "__main__":
    test()
    zipme.finish(__file__, allowed_imports={"flask", "html", "psycopg"})

# 55574554642200000000
