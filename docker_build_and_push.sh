#! /bin/bash

set -e

validate_var() {
    if [ -z "$1" ]; then
        echo "$2 must be defined."
        return 1
    else
        return 0
    fi
}

validate_var "$ECR_URI" "ECR_URI" || exit 1
validate_var "$TIMESTAMP" "TIMESTAMP" || exit 1
validate_var "$GIT_HASH" "GIT_HASH" || exit 1

IMAGE="${ECR_URI}"

echo "TIMESTAMP = ${TIMESTAMP}"
echo "GIT_HASH = ${GIT_HASH}"

TAG="${TIMESTAMP}-${GIT_HASH}"

echo "TAG = ${TAG}"

IMAGE_TAG="${IMAGE}:${TAG}"
IMAGE_TAG_LATEST="${IMAGE}:latest"

echo "IMAGE_TAG = ${IMAGE_TAG}"

PUSH="${PUSH:-'1'}"
LATEST="${LATEST:-'1'}"

docker build -t "${IMAGE_TAG}" -f ${DOCKER_FILE} .
if [ "$OSX" != "0" ] ; then
    echo "OSX IS NOT 0: FORCING SKIP DOCKER PUSH"
    PUSH=0
fi
if [ "$PUSH" = "1" ] ; then
    echo "DOCKER PUSH"
    docker push "${IMAGE_TAG}"
    if [ "$LATEST" = "1" ] ; then
        docker tag "${IMAGE_TAG}" "${IMAGE_TAG_LATEST}"
        docker push "${IMAGE_TAG_LATEST}"
    fi
else
    echo "DOCKER PUSH SKIPPED"
fi
