# EnviroLens Data Engineering Pipeline 

## Project Overview
This repository contains the backend data engineering pipeline for **EnviroLens**, a civic-tech application designed to monitor urban environmental metrics. This system acts as a 7-day pilot program for a municipality, designed to securely store and process massive batches of telemetry data (temperature, humidity, carbon monoxide, smoke) from city-wide IoT sensors. 

The architecture prioritizes idempotency, portability, and scalability. It utilizes a containerized Python ingestion script to batch-load over 400,000 records into a flexible NoSQL database.

## Architecture & Technology Stack
*   **Database:** MongoDB (NoSQL) - Chosen for its flexible document schema, allowing the seamless future integration of undefined sensor types without breaking the data model.
*   **Application Layer:** Python 3.9 (Pandas, PyMongo) - Ensures data is cleaned, transformed into JSON-compatible dictionaries, and idempotently loaded (wiping old batch states to prevent data duplication).
*   **Infrastructure:** Docker & Docker Compose - The entire system is fully containerized, ensuring hardware-independent deployment.
*   **Data Source:**  I used the “Environmental Sensor Telemetry Data” dataset from Kaggle. This dataset contains approximately 405,000 records of metrics from IoT devices, including temperature, humidity, carbon monoxide (CO), and light, which perfectly meets the project’s requirements.

## How to Run the Pipeline

This system is completely automated. You do not need to install Python or MongoDB locally to run it—you only need Docker Desktop application already installed. Click on this [Link](https://docs.docker.com/get-started/get-docker/) to go to the official website and download Docker Application.

**1. Clone the repository:**
```
git clone https://github.com/KushTrip/EnviroLens_Data_Engineering.git
cd EnviroLens_Data_Engineering
```
**2. Download the Dataset:**
Because the raw sensor dataset is ~62 MB, it is too large to be hosted directly in this code repository.
* Go to the [Kaggle Environmental Sensor Telemetry Dataset](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k/data)
* Download the archive and extract the CSV file.
* **Very Important**: Rename the extracted file to exactly **sensor_data.csv**.
* Place sensor_data.csv directly inside your cloned EnviroLens_Data_Engineering folder.

**3. Build and execute the system:**
```
docker compose up --build
```
**4. Expected Output:**
Docker will automatically pull the MongoDB image, build the Python environment, and execute ingest.py. You will see the container logs in your terminal confirming the successful database connection, the clearing of old data, and the insertion of 405,184 telemetry records. The Python container will gracefully exit with Code 0 upon completion.

**5. Shut down the environment:**
```
docker compose down
```

