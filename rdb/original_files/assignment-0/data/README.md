* `requirements.txt` contains the required Python libraries and versions for the assignments.
* The command `./docker_build.sh` builds a Docker image named `rddaimage` based on `Dockerfile`.
    * The command might not work on macOS due to a user id conflict, but Docker on macOS (supposedly) handles file permissions gracefully anyway. I have not tested it, but adding a user without a fixed `--uid` and `--gid` might work.
* The command `./run.sh` creates a Docker container based on the previously created `rddaimage`. Files from the current directory of the host system will be mapped to the `/data` directory of the container.
