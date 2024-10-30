# Build docker image named "rddaimage" with id of current user to avoid
# file permission conflicts.
docker build \
    --build-arg MY_USER_ID=1000 \
    --build-arg MY_GROUP_ID=1000 \
    --build-arg MY_USER_NAME=user$(shuf -i 10000000-99999999 -n 1) \
    --progress=plain \
    -t rddaimage .
