# Use an official Python runtime as a parent image
FROM python:3.11

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV DATABASE_URL="sqlite+aiosqlite:///.//pytest/data/test.db"
ENV API_KEY_SECRET="laisjdf;asdifj[fi9wejr'wekf]"
ENV ENCRYPTION_KEY_SECRET="alsk;fj2 i3jeqealfjansdflkmadf"

# Copy the entrypoint script into the container
COPY dockerfile_pytest_app_entrypoint.sh /usr/src/app/

# Ensure the script has Unix line endings
RUN apt-get update && apt-get install -y dos2unix && dos2unix /usr/src/app/dockerfile_pytest_app_entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/src/app/dockerfile_pytest_app_entrypoint.sh

# Run the entrypoint script when the container launches
ENTRYPOINT ["/usr/src/app/dockerfile_pytest_app_entrypoint.sh"]