# Use an Alpine image with Python 3.12.5
FROM python:3.12.5-alpine

# Install tzdata for time zone configuration
RUN apk add --no-cache tzdata

# Set the time zone
ENV TZ=Europe/Amsterdam

# Set the working directory in the container
WORKDIR /app

# Install necessary system libraries
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . .

# Set the command to run the script
CMD ["python", "tibber_energy_monitor.py"]
