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
        print("\n1. Clearing old data to prevent duplicates...")
        collection.delete_many({})

        # Step B: Read the CSV file into a DataFrame
        print("\n2. Reading CSV file (this might take a few seconds for 405k rows)...")
        df = pd.read_csv('sensor_data.csv')

        # Step B2: Check if the file is completely empty
        if df.empty:
            print("\nFAILURE: The file 'sensor_data.csv' exists but contains zero data rows. Aborting batch job.")
            return  # This stops the script safely

        # Step C: Data Quality check to ensure the DataFrame is not empty
        print("\n3. Scanning for missing values and half-broken rows...")
        initial_row_count = len(df)

        # Drop any row with missing value 
        df_cleaned = df.dropna()
        cleaned_row_count = len(df_cleaned)

        # calculate and log the broken rows
        broken_rows = initial_row_count - cleaned_row_count
        if broken_rows > 0:
            print(f"\n  -> WARNING: {broken_rows} rows were dropped due to missing values.")
        else:
            print("\n  -> SUCCESS: Data is 100% clean with no missing values.")

        # Step D: Transform the DataFrame to match the MongoDB schema
        print("\n4. Transforming data to match MongoDB document format...")
        data_dict = df_cleaned.to_dict("records")

        # Step E: Load the transformed data into MongoDB
        print("\n5. Inserting massive Batch of data into MongoDB...")
        collection.insert_many(data_dict)
    
        # Step F: Verify the insertion by counting the documents in the collection
        total_records = collection.count_documents({})
        print(f"\nSUCCESS: {total_records} clean records inserted into EnviroLens DB!")

    except FileNotFoundError:
        print("\nERROR: The file 'sensor_data.csv' was not found. Please ensure the file exists in the correct directory.")
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_batch_job()
