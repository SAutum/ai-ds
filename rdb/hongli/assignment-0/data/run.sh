# Run docker container based on "rddaimage".
#
# --rm
#     Remove container after exit to avoid wasting memory.
#
# -ti
#     Interactive
#
# -v "$PWD":/data
#     Map the current directory of the host into the docker container at "/data"
#
docker run \
    --rm \
    -it \
    -v "$PWD":/data \
    rddaimage
