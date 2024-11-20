# Run docker container based on "rddaimage".
#
# --rm
#     Remove container after exit to avoid wasting memory.
#
# -ti
#     Interactive
#
# -v "$PWD":/data
#     Map the current directory of the host into the docker container at "/data".
#     You will not be able to access any files above in the folder hierarchy,
#     so make sure to run this docker run command where your files are.
#
docker run \
    --rm \
    -it \
    -v "$PWD":/data \
    rddaimage
