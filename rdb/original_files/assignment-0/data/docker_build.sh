# Build docker image named "rddaimage" with id of current user to avoid
# file permission conflicts.
# On MacOS, file permissions are handled differently, but the user id
# might collide with the host user. In case of MacOS,
# remove uid and gid from adduser in Dockerfile.
docker build \
    --build-arg MY_USER_ID=$(id -u) \
    --build-arg MY_GROUP_ID=$(id -g) \
    --build-arg MY_USER_NAME=user$(shuf -i 10000000-99999999 -n 1) \
    --progress=plain \
    -t rddaimage .
