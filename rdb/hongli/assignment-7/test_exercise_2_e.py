import hashlib
import zipme

filename = "exercise_2_e.txt"

cube_lines = """\
                        +-----------+-----------+-----------+
                       /11111111111/22222222222/33333333333/|
                      /11111111111/22222222222/33333333333/3|
                     /11111111111/22222222222/33333333333/33|
                    +-----------+-----------+-----------+333|
                   /44444444444/55555555555/66666666666/|333|
                  /44444444444/55555555555/66666666666/6|333+
                 /44444444444/55555555555/66666666666/66|33/|
                +-----------+-----------+-----------+666|3/h|
               /77777777777/88888888888/99999999999/|666|/hh|
              /77777777777/88888888888/99999999999/9|666+hhh|
             /77777777777/88888888888/99999999999/99|66/|hhh|
            +-----------+-----------+-----------+999|6/g|hhh+
            |77777777777|88888888888|99999999999|999|/gg|hh/|
            |77777777777|88888888888|99999999999|999+ggg|h/j|
            |77777777777|88888888888|99999999999|99/|ggg|/jj|
            |77777777777|88888888888|99999999999|9/c|ggg+jjj|
            |77777777777|88888888888|99999999999|/cc|gg/|jjj|
            +-----------+-----------+-----------+ccc|g/i|jjj+
            |aaaaaaaaaaa|bbbbbbbbbbb|ccccccccccc|ccc|/ii|jj/
            |aaaaaaaaaaa|bbbbbbbbbbb|ccccccccccc|ccc+iii|j/
            |aaaaaaaaaaa|bbbbbbbbbbb|ccccccccccc|cc/|iii|/
            |aaaaaaaaaaa|bbbbbbbbbbb|ccccccccccc|c/f|iii+
            |aaaaaaaaaaa|bbbbbbbbbbb|ccccccccccc|/ff|ii/
            +-----------+-----------+-----------+fff|i/
            |ddddddddddd|eeeeeeeeeee|fffffffffff|fff|/
            |ddddddddddd|eeeeeeeeeee|fffffffffff|fff+
            |ddddddddddd|eeeeeeeeeee|fffffffffff|ff/
            |ddddddddddd|eeeeeeeeeee|fffffffffff|f/
            |ddddddddddd|eeeeeeeeeee|fffffffffff|/
            +-----------+-----------+-----------+
""".rstrip().split("\n")


def test() -> None:
    expected_solutions = """
    333bf9f839ac958591c1d8b15f02c55b7e673f45bb0f1b1df823c0e55a14c523
    52ef3fda2a012f836019011a0b2e76c3eb1e5ec1c19eef3803da54b23f10a722
    690b5d70131877de2522365f8b1cd9f95b7c76362dae8e14bc9dfcf197b650bb
    6aa88df6bbc0b0cba164b4783d2c5931a20113c528e8f69a045f8d22ebe5e8e7
    c4633a84e316b2c0520a05aae5cb8af15bb96dc53c93124fff6fe25e97ced8cb
    270b5417477ab78c9af0d92e123dbadca6cd43531be5aa79f70386976a65c512
    d356a651f64d8fc8ce03d2d85ef52998ac50f175a0210e7126bdfde5f871f803
    2c6127486f8ff62f505040c28c1eec17d32bda282bb82b42a23c6a1ad8d20d33
    acbc20436fa39cee55b0f8ef5dc2fd2b01f4fd2ad215331bd847861600e47685
    """

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    # Remove comments
    lines = [line.split("#")[0].rstrip() for line in lines]

    # Discard empty lines
    lines = [line for line in lines if line]

    assert (
        len(lines) % len(cube_lines) == 0
    ), f"File {filename} has {len(lines)} non-comment non-empty lines, but it should have a multiple of {len(cube_lines)} lines, because each cube has {len(cube_lines)} lines."

    i_line = 0
    solutions = set()
    for i_cube in range(1, 1 + 4):
        # Scan cube to find out which faces have been marked
        marked_set = set()
        for cube_line in cube_lines:

            if i_line >= len(lines):
                raise ValueError(f"Cube line {i_line + 1} of cube {i_cube} is incomplete")

            line = lines[i_line]
            i_line += 1

            for i, c in enumerate(cube_line):
                d = line[i]

                # Check if structure of cube has been distorted
                if c in "+-/|":
                    if d != c:
                        raise ValueError(
                            f'Expected a "{c}" character at line {i_line}, char {i + 1} of {filename} instead of "{d}" in cube {i_cube}'
                        )

                # Check if face has been marked
                if d not in "+-/| ":
                    if c not in "123456789abcdefghij":
                        raise ValueError(
                            f'Can not mark line {i_line}, char {i + 1} of {filename} with "{d}" in cube {i_cube}.'
                        )

                    marked_set.add(c)

        marked = "".join(sorted(marked_set))

        marked_faces = ", ".join(marked)

        print(f"You have marked the faces {marked_faces} of cube {i_cube}:\n")

        # Mark all characters of face
        marked_cube = "\n".join("".join(c if c in marked or c in "+ -/|" else " " for c in line) for line in cube_lines)

        print(marked_cube, end="\n\n")

        h = hashlib.sha256(marked_cube.encode("utf-8")).hexdigest()

        assert h in expected_solutions, f"You did not correctly mark a slice of cube {i_cube}."

        solutions.add(h)

    print(f"In total, {len(solutions)} unique slices have been marked.\n")

    assert len(solutions) == 4, "You did not mark four unique slices."


if __name__ == "__main__":
    test()
    zipme.finish(filename, min_size=1000, max_size=20_000)

# 32233407402000000000
