# 1. Use an official, lightweight Python image.
FROM python:3.11-slim

# 2. Create a working directory inside the container.
WORKDIR /app

# 3. Copy the requirements file into the container.
COPY requirements.txt .

# 4. Install the dependencies from the requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our files (the CSV and python script) into the container.
COPY . .

# 6. Set the command to run the Python script when the container starts.
CMD ["python", "ingest.py"]
