#!/bin/bash

# Load environment variables from the .env file
if [ -f .env ]; then
  source .env
else
  echo "Error: .env file not found."
  exit 1
fi

# List of required environment variables
REQUIRED_VARS=("APP_NAME" "APP_PATH" "APP_LANG" "APP_NETWORK")

# Check if each required variable is set
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Error: $var is not set in the .env file."
    exit 1
  fi
done

IMAGE_NAME="${APP_NAME}-${APP_LANG}"

# Stop and remove the existing container if it’s running
if [ "$(docker ps -q -f name=${IMAGE_NAME})" ]; then
  echo "Stopping existing container ${IMAGE_NAME}..."
  docker stop ${IMAGE_NAME}
fi

if [ "$(docker ps -aq -f name=${IMAGE_NAME})" ]; then
  echo "Removing existing container ${IMAGE_NAME}..."
  docker rm ${IMAGE_NAME}
fi

# Run the Docker container
docker run --name ${IMAGE_NAME} -it -d \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -v "${APP_PATH}:/app" \
  -w /app \
  --network ${APP_NETWORK} \
  ${IMAGE_NAME} supervisord

# Check if the container started successfully
if [ $? -eq 0 ]; then
  echo "Docker container '${IMAGE_NAME}' started successfully."
else
  echo "Error: Failed to start Docker container '${IMAGE_NAME}'."
  exit 1
fi
