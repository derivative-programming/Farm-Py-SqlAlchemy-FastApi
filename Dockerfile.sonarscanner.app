# Use the official Python image as a base image
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SonarScanner and JDK
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk-headless wget unzip && \
    wget -O sonar-scanner-cli.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747-linux.zip && \
    unzip sonar-scanner-cli.zip -d /opt && \
    mv /opt/sonar-scanner-4.7.0.2747-linux /opt/sonar-scanner && \
    rm sonar-scanner-cli.zip && \
    ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the wait script into the container
COPY wait-for-sonarqube.sh /usr/src/app/

# Make the script executable
RUN chmod +x /usr/src/app/wait-for-sonarqube.sh

# Copy the rest of the application code into the container
COPY . .

# Define the entrypoint
ENTRYPOINT ["/usr/src/app/wait-for-sonarqube.sh"]