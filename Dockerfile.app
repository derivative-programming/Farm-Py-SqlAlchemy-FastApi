# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV DATABASE_URL="sqlite+aiosqlite:///./test.db"
ENV API_KEY_SECRET="laisjdf;asdifj[fi9wejr'wekf]"
ENV ENCRYPTION_KEY_SECRET="alsk;fj2 i3jeqealfjansdflkmadf"

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]