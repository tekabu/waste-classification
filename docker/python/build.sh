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

# Define the path to the requirements.txt file
REQUIREMENTS_FILE="${APP_PATH}/requirements.txt"

# Check if the source file exists
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "File $REQUIREMENTS_FILE found. Copying to Docker image build context..."
  cp "$REQUIREMENTS_FILE" "./requirements.txt"
else
  echo "File $REQUIREMENTS_FILE not found. Creating an empty file..."
  touch "./requirements.txt"
fi

# Construct the image name using the APP_NAME and APP_LANG
IMAGE_NAME="${APP_NAME}-${APP_LANG}"

# Build the Docker image with the specified arguments
docker build --build-arg APP_PATH="$APP_PATH" -t "${IMAGE_NAME}" -f ./Dockerfile .

# Check if the image build was successful
if [ $? -eq 0 ]; then
  echo "Docker image '${IMAGE_NAME}' built successfully."
else
  echo "Error: Failed to build image '${IMAGE_NAME}'."
  exit 1
fi
