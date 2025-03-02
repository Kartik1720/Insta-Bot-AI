# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y chromium chromium-driver

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Railway uses
EXPOSE 8080

# Start the application
CMD ["python", "main.py"]

RUN chmod +x start.sh
CMD ["./start.sh"]
