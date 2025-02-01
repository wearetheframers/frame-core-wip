# Core stage
FROM python:3.10-slim as core

# Set the working directory
WORKDIR /app

# Copy only core requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package files
COPY . .

# Install the core package
RUN pip install .

# Plugin stage
FROM core as plugins

# Install plugin requirements
COPY requirements-plugins.txt .
RUN pip install --no-cache-dir -r requirements-plugins.txt

# Development stage
FROM plugins as dev

# Install development requirements
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Default to core stage
FROM core

# Make port 80 available
EXPOSE 80

# Run the application
CMD ["python", "-m", "frame.cli.cli"]
