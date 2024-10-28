import ast
import io
import os
import re
import numpy as np
import platform
import random
import shutil
import subprocess
import sys
import tarfile
import time
import tracemalloc
import zlib
from pathlib import Path
from typing import List, Dict, Set, Optional

all_imports = """
array
ast
base64
binascii
bisect
bz2
calendar
cmath
codecs
collections
colorsys
copy
csv
datetime
decimal
enum
flask
fractions
functools
glob
graphlib
gzip
hashlib
heapq
hmac
html
io
itertools
itsdangerous
jinja2
json
keyword
lzma
math
matplotlib
mmap
multiprocessing
numpy
operator
pathlib
pprint
psycopg
queue
random
re
secrets
shutil
socket
sqlite3
stat
statistics
string
struct
tarfile
threading
time
timeit
token
tokenize
trace
tracemalloc
turtle
types
typing
urllib
uuid
wave
werkzeug
xml
zipfile
zlib
zoneinfo
"""

library_versions = """
click==8.1.7
contourpy==1.3.0
cycler==0.12.1
Flask==3.0.3
fonttools==4.54.1
gunicorn==23.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
kiwisolver==1.4.7
MarkupSafe==2.1.5
matplotlib==3.9.2
numpy==2.1.1
packaging==24.1
pillow==10.4.0
psycopg==3.2.3
psycopg-binary==3.2.3
pyparsing==3.1.4
python-dateutil==2.9.0.post0
six==1.16.0
typing_extensions==4.12.2
Werkzeug==3.0.4
"""

start_time = time.perf_counter()


def begin_testing() -> None:
    # Seed random number generators for reproducibility
    random.seed(0)
    np.random.seed(0)

    # Check operating system
    operating_system = platform.system()

    if operating_system != "Linux":
        print_red(
            f"WARNING: It seems that you are running this script on {operating_system}. This script is designed to run on Linux."
        )

    # Begin memory profiling
    tracemalloc.start()


def finish(
    filename: str,
    max_seconds: float = 30.0,
    max_memory: float = 1e9,
    allowed_imports: Set[str] = set(all_imports.strip().split()),
    disallowed_imports: Set[str] = set(),
    disallowed_identifiers: Set[str] = set(),
    min_size: int = 10,
    max_size: int = 10**6,
) -> None:
    # End memory profiling
    _, peak = tracemalloc.get_traced_memory()

    assert (
        peak <= max_memory
    ), f"Your solution uses {peak*1e-6:.3f} MB of memory, which is more than the allowed maximum of {max_memory*1e-6:.3f} MB for this exercise."

    tracemalloc.stop()

    # Check execution time
    elapsed_time = time.perf_counter() - start_time

    assert (
        elapsed_time <= max_seconds
    ), f"Your solution took {elapsed_time:.3f} seconds to run, which is more than the allowed maximum of {max_seconds:.3f} seconds for this exercise."

    # If filename of test is given, test same filename without "test_" instead
    if re.match(r".*test_exercise_.*\.py$", filename):
        filename = os.path.basename(filename)[len("test_") :]

    if Path(filename).suffix in [".md", ".txt", ".png", ".pdf"]:
        check_file_size(filename, min_size, max_size)
        return

    # Check Python source code for disallowed identifiers and modules
    allowed_imports = allowed_imports - disallowed_imports

    disallowed_identifiers |= {
        "__import__",
        "__class__",
        "__mro__",
        "__bases__",
        "__globals__",
        "__subclasses__",
        "__module__",
        "__builtin__",
        "__builtins__",
        "exec",
        "eval",
        "exit",
    }

    code = Path(filename).read_text(encoding="utf-8")

    lines = code.splitlines()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        # Check for disallowed identifiers
        name = None
        line = ""
        if isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.FunctionDef):
            name = node.name
        elif isinstance(node, ast.Attribute):
            name = node.attr

        if name is not None:
            line = lines[node.lineno - 1]
            assert (
                name not in disallowed_identifiers
            ), f'"{name}" in line {node.lineno} is not allowed for this exercise.\n\n{line}'

        if isinstance(node, ast.alias):
            assert node.name not in disallowed_identifiers, f'"{node.name}" is not allowed for this exercise.'

        # Check for disallowed modules
        if isinstance(node, ast.Import):
            line = lines[node.lineno - 1]
            for node_name in node.names:
                module = node_name.name.split(".")[0]
                assert module in allowed_imports, (
                    f"Import of {module} module in line {node.lineno} of file {filename} not allowed for this exercise. Allowed imports for this exercise are:\n\n"
                    + ", ".join(sorted(allowed_imports))
                )

        if isinstance(node, ast.ImportFrom):
            line = lines[node.lineno - 1]
            if not node.module:
                continue
            module = node.module.split(".")[0]
            assert module in allowed_imports, (
                f"Import of {module} module in line {node.lineno} of file {filename} not allowed for this exercise. Allowed imports for this exercise are:\n\n"
                + ", ".join(sorted(allowed_imports))
            )

    # Check common mistakes

    # Check if np.vectorize was used
    assert (
        "np.vectorize" not in code
    ), 'Do not use the function np.vectorize. See docs: "The vectorize function is provided primarily for convenience, not for performance. The implementation is essentially a for loop."'

    # Check if parameters are passed to psycopg
    match = re.match(r"psycopg.connect\(.+?\)", code, flags=re.DOTALL)
    if match:
        print_red(
            f"It looks like you are passing parameters to {match}. This will break our tests and your solution will not work. Instead, use environment variables like PGUSER to configure your connection."
        )

    # Check if tests have been modified
    for testfile in sorted(Path(".").glob("test_*.py")):
        data = testfile.read_bytes()

        if zlib.crc32(data) != 0:
            print_red(f"WARNING: It seems that you have modified {testfile}. This is not allowed.")

    print(f"Peak memory usage {peak*1e-6:.3f} MB, execution time {elapsed_time:.3f} seconds")
    print("Tests passed :)")


def check_no_for_loops(filename: str) -> None:
    text = Path(filename).read_text(encoding="utf-8")

    lines = text.splitlines()
    tree = ast.parse(text)
    for node in ast.walk(tree):
        assert not isinstance(
            node, ast.For
        ), f"For loop in line {node.lineno} of file {filename} not allowed for this exercise:\n\n{lines[node.lineno - 1]}"
        assert not isinstance(
            node, ast.While
        ), f"While loop in line {node.lineno} of file {filename} not allowed for this exercise:\n\n{lines[node.lineno - 1]}"
        assert not isinstance(
            node, ast.ListComp
        ), f"List comprehension in line {node.lineno} of file {filename} not allowed for this exercise (does not offer increased performance compared to a for-loop):\n\n{lines[node.lineno - 1]}"


def test_checksum(filename: str) -> None:
    data = Path(filename).read_bytes()

    checksum_ok = zlib.crc32(data) == 0

    assert checksum_ok, f"Modifying {filename} is forbidden! Forbidden!"


def print_red(msg: str) -> None:
    print(f"\033[91m{msg}\033[0m")


def print_log(log: List[str], msg: str) -> None:
    print(msg)
    log.append(msg)


def print_log_red(log: List[str], msg: str) -> None:
    print(f"\033[91m{msg}\033[0m")
    log.append(msg)


def read_versions(text: str) -> Dict[str, str]:
    versions = dict(line.split("==") for line in text.strip().replace("\r", "").split("\n") if line.count("==") == 1)
    return versions


def decode_utf8(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        msg = f"ERROR: Failed to decode bytes as UTF-8:\n{repr(data)}\n"
        print_red(msg)
        return msg


def check_file_size(filename: str, min_size: int, max_size: int) -> None:
    assert Path(filename).is_file(), f"File {filename} does not exist."

    size = Path(filename).stat().st_size

    assert (
        size >= min_size
    ), f"File {filename} is smaller than expected ({size} bytes). Expected at least {min_size} bytes."
    assert (
        size <= max_size
    ), f"File {filename} is larger than expected ({size} bytes). Expected no more than {max_size} bytes."

    print(f"File {filename} exists. Content will be checked manually after the deadline.")


begin_testing()


def test_and_zip(assignment: str = "rdda-2", max_size: int = 4 * 10**6) -> None:
    filenames = """
        data
        exercise_1_a.py
        exercise_1_b.py
        exercise_1_c.py
        exercise_1_d.py
        exercise_1_e.py
        exercise_1_f.py
        exercise_1_g.txt
        exercise_2.py
        test_exercise_1_a.py
        test_exercise_1_b.py
        test_exercise_1_c.py
        test_exercise_1_d.py
        test_exercise_1_e.py
        test_exercise_1_f.py
        test_exercise_2.py
        zipme.py""".strip().split()

    # Check if zipme.py has been modified
    test_checksum("zipme.py")

    # Find new version number
    version = 1
    while True:
        directory = Path(f"{assignment}-version-{version:02d}")
        archive = directory.with_suffix(".tar.gz")

        if not directory.exists() and not archive.exists():
            break

        version += 1

    log: List[str] = []

    # Test Python version
    if sys.version_info.major != 3 or sys.version_info.minor != 10:
        print_log_red(
            log,
            f"You are running Python {sys.version} instead of 3.10.*. Make sure your code also works with Python 3.10, or you will not get any points.",
        )

    command = [sys.executable, "-m", "pip", "list", "--format=freeze"]
    pip_freeze_output = subprocess.check_output(command).decode("utf-8")
    installed_versions = read_versions(pip_freeze_output)

    incorrect_versions_list = []

    for library, library_version in read_versions(library_versions).items():
        if library not in installed_versions:
            print_log_red(log, f"WARNING: Library {library} is not installed.")
        elif installed_versions[library] != library_version:
            incorrect_versions_list.append(f"{library} {installed_versions[library]} instead of {library_version}")

    if incorrect_versions_list:
        incorrect_versions = ", ".join(incorrect_versions_list)
        print_log_red(
            log,
            f"WARNING: Some libraries have incorrect versions: {incorrect_versions}. We will not fix your code if it does not work with the required version.",
        )

    # Create new assignment directory
    print_log(log, f"Copying files to {directory} test directory.")
    directory.mkdir()

    # Copy files
    for src in filenames:
        dst = directory / src

        if Path(src).is_file():
            shutil.copy2(src, dst)
        elif Path(src).is_dir():
            shutil.copytree(src, dst)
        else:
            print_log_red(log, f"File {src} not found.")

    # Run tests
    num_passed = 0
    num_tests = 0
    for filename in filenames:
        if not filename.startswith("test_exercise_"):
            continue

        num_tests += 1

        if not Path(filename).is_file():
            continue

        test_checksum(filename)

        print_log(log, f"Running test {filename} in {directory} directory.")

        # Start new process for test
        process = subprocess.Popen(
            [sys.executable, filename],
            cwd=directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait until process is finished
        stdout, stderr = process.communicate()

        # Check if process finished successfully
        if process.returncode != 0:
            print_log_red(log, f"Test {filename} failed.")
            print_log_red(log, decode_utf8(stdout))
            print_log_red(log, decode_utf8(stderr))
        else:
            print_log(log, f"Test {filename} passed.")
            print_log(log, decode_utf8(stdout))
            print_log(log, decode_utf8(stderr))
            num_passed += 1

    print_log(log, f"Passed {num_passed} of {num_tests} automated tests.")

    # Praise student if all tests passed
    if num_passed == num_tests:
        print_log(log, "\n\033[32mVery good!\033[0m 👍\n")

    def tar_filter(info: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
        # Exclude large files from tar archive
        if info.name in []:
            return None
        return info

    # Create archive
    print_log(log, f"Creating archive {str(archive)} for upload.\n")
    with tarfile.open(archive, "w:gz", compresslevel=9) as t:
        t.add(directory, filter=tar_filter)
        logdata = "\n".join(log).encode("utf-8")
        info = tarfile.TarInfo(f"{directory}/.error_log")
        info.size = len(logdata)
        t.addfile(info, io.BytesIO(logdata))

    # Complain about files which are too large
    size = archive.stat().st_size

    assert (
        size <= max_size
    ), f"Your submission is too large. The maximum is {max_size*1e-6} MB, but your submission is {size*1e-6:.6f} MB."

    # Cleanup
    shutil.rmtree(directory)


if __name__ == "__main__":
    test_and_zip()

# 73402653122200000000
