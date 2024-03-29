# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=run
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Run the command to start the Flask app
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]
