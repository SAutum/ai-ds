import sys
import zipme
import traceback
import urllib.request
from test_exercise_2_a import spawn_server, check_database_connection


def test() -> None:
    host = "127.0.0.1"
    port = 5000

    command = [sys.executable, "-m", "gunicorn", "--reuse-port", "--bind", f"{host}:{port}", "exercise_2:app"]
    spawn_server(command, host, port)
    check_database_connection()

    url = f"http://{host}:{port}/year-state"

    try:
        with urllib.request.urlopen(url) as r:
            html = r.read().decode("utf-8")
            # Simplify HTML for more robust testing
            html = html.lower().replace(",", "").replace(".", "")
    except urllib.error.HTTPError:
        traceback.print_exc()
        print_red(f"ERROR: Could not open {url}")
        sys.exit(1)

    for substring in ["state", "2015", "2020", "berlin", "saarland", "55718", "578191"]:
        assert (
            substring in html
        ), f"Could not find {substring} in {url} (ignoring punctuation, comparing case insensitive)"


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[0m")


if __name__ == "__main__":
    test()
    zipme.finish("exercise_2.py")

# 14064324362000000000
