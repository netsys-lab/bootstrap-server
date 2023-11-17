# Use Python on Alpine as base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the script into the container
COPY filewatcher.py .

# Command to run the script
CMD [ "python", "./filewatcher.py" ]