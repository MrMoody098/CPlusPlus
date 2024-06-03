# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install NGINX
RUN apt-get update && apt-get install -y nginx

# Remove the default NGINX configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the NGINX configuration file
COPY nginx.conf /etc/nginx/sites-available/

# Create a symlink to the NGINX configuration file
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

# Expose port 80
EXPOSE 80

# Start NGINX and your Flask application
CMD service nginx start && flask run --host=0.0.0.0
