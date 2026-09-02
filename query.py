import pymongo

# connect to the mongodb container
client = pymongo.MongoClient("mongodb://envirolens_db:27017/")
db = client["envirolens_db"]
collection = db["sensor_telemetry"]

print("\n ENVIROLENS DB QUERIES")

# ---User story 1: City Planner (Max Temperature)---
print("\nExecuting User Story 1: City Planner (Max Temperature)")
# We sort the temperature in descending order and limit the result to 1 to get the maximum temperature recorded
highest_temp_doc = collection.find_one({}, sort=[("temp", -1)])

print(f"Highest temperature recorded: {highest_temp_doc['temp']}°C in Berlin city")
print(f"Device: {highest_temp_doc['device']}")
print(f"Timestamp: {highest_temp_doc['ts']}")

# ---User story 2: Citizen ---
print("\nExecuting User Story 2: Citizen (Latest Air Quality at Transit Hub)")
# We filter for the specific variable sensor (device 1c:bf:ce:15:ec:4d)
# Then we sort by timestamp ('ts') in descending order to get the newest reading
query_filter = {"device": "1c:bf:ce:15:ec:4d"}
latest_reading = collection.find_one(query_filter, sort=[("ts", -1)])

print(f"Result: Latest readings for transit hub sensor at {latest_reading['ts']}:") # timestamp of the latest reading
print(f"Smoke Level: {latest_reading['smoke']}")
print(f"Carbon Monoxide (CO): {latest_reading['co']}")
print(f"Humidity: {latest_reading['humidity']}")

print("\nAll queries executed successfully.")
