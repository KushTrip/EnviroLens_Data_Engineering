import pandas as pd
from pymongo import MongoClient

# 1. connect to the docker database
MONGO_URI = "mongodb://envirolens_db:27017/"
client = MongoClient(MONGO_URI)

# 2. create a database and collection
db = client['envirolens_db']
collection = db['sensor_telemetry']

def run_batch_job():
    try:
        # Step A: Enforce Idempotency by dropping the collection if it exists
        print("1. Clearing old data to prevent duplicates...")
        collection.delete_many({})

        # Step B: Read the CSV file into a DataFrame
        print("2. Reading CSV file (this might take a few seconds for 405k rows)...")
        df = pd.read_csv('sensor_data.csv')

        # Step C: Transform the DataFrame to match the MongoDB schema
        print("3. Transforming data to match MongoDB document format...")
        data_dict = df.to_dict("records")

        # Step D: Load the transformed data into MongoDB
        print("4. Inserting massive Batch of data into MongoDB...")
        collection.insert_many(data_dict)

        # Step E: Verify the insertion by counting the documents in the collection
        total_records = collection.count_documents({})
        print(f"SUCCESS: {total_records} records inserted into EnviroLens DB!")

    except FileNotFoundError:
        print("ERROR: The file 'sensor_data.csv' was not found. Please ensure the file exists in the correct directory.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_batch_job()
