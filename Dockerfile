# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Ensure the scripts directory is copied
COPY scripts /app/scripts

# Make the script executable
RUN chmod +x /app/scripts/setup_environment.sh

# Run the script to select the appropriate requirements file
RUN /bin/bash /app/scripts/setup_environment.sh

# Install any needed packages specified in the selected requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application
CMD ["python", "-m", "frame.cli.cli"]
