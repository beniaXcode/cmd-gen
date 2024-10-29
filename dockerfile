# Use the official Python image as a base
FROM python:3.10-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/beniaXcode/cmd-gen.git .

# Copy requirements.txt to the container
# (Since the requirements.txt is in the cloned repo, we don't need to copy it separately)
# If the requirements.txt is in a different path in the repo, adjust accordingly
# COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=command.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["flask", "run"]
