# Use the official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask to run the app
ENV FLASK_APP=app.py

# Expose port 4500 for Flask app
EXPOSE 4500

# Run the command to start the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=4500"]
