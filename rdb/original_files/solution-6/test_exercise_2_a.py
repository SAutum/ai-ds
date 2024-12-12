import os
import sys
import time
import zipme
import atexit
import signal
import socket
import typing
import psycopg
import threading
import traceback
import subprocess
import urllib.request


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


def spawn_server(
    command: list[str], host: str, port: int, timeout: float = 2.0
) -> None:
    # Check if no server is started yet
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        if 0 == sock.connect_ex((host, port)):
            print_red(
                f"Port {port} already in use. Please stop whatever is using this port and try again."
            )
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
    def kill():
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
    host = "127.0.0.1"
    port = 5000

    # Spawn server using gunicorn.
    # "--reuse-port" might not be a good idea in practice since it might allow
    # other processes to hijack a port, but for testing it is probably fine.
    command = [sys.executable, "-m", "gunicorn", "--reuse-port", "--bind", f"{host}:{port}", "exercise_2:app"]
    spawn_server(command, host, port)
    check_database_connection()

    tables = {
        "timestamp": [
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "quarter",
            "weekday",
            "isotime",
        ],
        "sale": ["sale_id", "shop_id", "product_id", "timestamp_id", "quantity"],
        "shop": [
            "shop_id",
            "branch",
            "state",
            "city",
            "city_population",
            "city_area",
            "city_geolocation",
        ],
        "product": [
            "product_id",
            "name",
            "rating",
            "price",
            "reviews",
            "category",
            "subcategory",
        ],
    }

    for table, attributes in tables.items():
        length_previous_html = 0
        for n in [1, 5, 13, 42]:
            url = f"http://{host}:{port}/table/{table}/{n}"

            print(f"Testing {url}")

            try:
                with urllib.request.urlopen(url) as r:
                    html = r.read().decode("utf-8").lower()
            except urllib.error.HTTPError:
                traceback.print_exc()
                print_red(f"ERROR: Could not open {url}")
                sys.exit(1)

            for attribute in attributes:
                assert (
                    attribute in html
                ), f"Could not find attribute {attribute} for table {url}"

            if length_previous_html >= len(html):
                print_red(
                    f"ERROR: Requested more rows than previously ({length_previous_html} characters), but somehow there are not more characters now ({len(html)})."
                )
                sys.exit(1)

            length_previous_html = len(html)

    url = f"http://{host}:{port}/table/product/1"

    escaped_product_names = [
        "Drill America - DWT54027 #0-80 UNF High Speed Steel Bottoming Tap, (Pack of 1) &lt;script&gt;alert(&#x27;Did you think about XSS and SQL injection?&#x27;)&lt;/script&gt;",
        "Drill America - DWT54027 #0-80 UNF High Speed Steel Bottoming Tap, (Pack of 1) &lt;script&gt;alert(&#39;Did you think about XSS and SQL injection?&#39;)&lt;/script&gt;",
        "Drill America - DWT54027 #0-80 UNF High Speed Steel Bottoming Tap, (Pack of 1) &lt;script&gt;alert('Did you think about XSS and SQL injection?')&lt;/script&gt;",
    ]

    with urllib.request.urlopen(url) as r:
        html = r.read().decode("utf-8")

    msg = f"Could not find escaped product name on page {url} in html shown below. If you found a different way to escape the product name, please let us know and we might add it to the tests. Currently, escaped names are:\n\n"
    msg += "\n".join(escaped_product_names)
    msg += "\n\n\n" + html

    if not any(name in html for name in escaped_product_names):
        print_red(msg)
        sys.exit(1)


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[0m")


if __name__ == "__main__":
    test()
    zipme.finish("exercise_2.py")

# 50464353100200000000
