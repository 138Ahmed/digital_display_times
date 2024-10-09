# Use the official Python image with version 3.13.0
FROM python:3.13.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . .

# Command to run Python script
CMD ["python", "process_prayer_times.py"]