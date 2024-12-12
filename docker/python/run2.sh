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

export DISPLAY=:0

xhost +local:docker

# Run the Docker container
docker run --name ${IMAGE_NAME} -it --rm \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -v "${APP_PATH}:/app" \
  -w /app \
  --network ${APP_NETWORK} \
  --device=/dev/ttyACM0:/dev/ttyUSB0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -p 8000:8000 \
  ${IMAGE_NAME} bash

# Check if the container started successfully
if [ $? -eq 0 ]; then
  echo "Docker container '${IMAGE_NAME}' started successfully."
else
  echo "Error: Failed to start Docker container '${IMAGE_NAME}'."
  exit 1
fi
