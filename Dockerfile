FROM $DOCKER_BASE:$BASE_TAG

# Copy function code to container
COPY $LAMBDA_FILE ./

# setting the CMD
CMD ["$LAMBDA_HANDLER"]
