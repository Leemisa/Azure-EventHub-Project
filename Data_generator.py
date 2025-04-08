import json  # To format our data as JSON
import time  # To add delay (simulate streaming)
import random  # To generate random values for location, speed, etc.
from faker import Faker  # To create fake/realistic-looking data
from datetime import datetime  # To get current time in ISO format

# Create a Faker instance to generate dummy data
fake = Faker()

# Function to generate a single data point for a given vehicle
def generate_data(vehicle_id):
    return {
        "vehicle_id": vehicle_id,  # Unique ID of the taxi/vehicle
        "latitude": round(random.uniform(-34.0, -22.0), 6),  # Random latitude (South Africa range)
        "longitude": round(random.uniform(18.0, 32.0), 6),  # Random longitude (South Africa range)
        "speed_kmh": round(random.uniform(0, 120), 2),  # Random speed between 0-120 km/h
        "status": random.choice(["en route", "idle", "maintenance"]),  # Random status
        "timestamp": datetime.utcnow().isoformat()  # Current UTC time in ISO format
    }

# Function to simulate continuous data streaming for multiple vehicles
def stream_data(num_vehicles=5, interval=2):
    # Create a list of vehicle IDs like Taxi-1, Taxi-2, etc.
    vehicle_ids = [f"Taxi-{i+1}" for i in range(num_vehicles)]
    
    # Keep generating and printing data until you stop the script
    while True:
        for vehicle_id in vehicle_ids:
            data = generate_data(vehicle_id)  # Generate data for each vehicle
            print(json.dumps(data))  # Print the data as a JSON string (simulating a stream)
        
        time.sleep(interval)  # Wait for 'interval' seconds before next batch

# Entry point of the script
if __name__ == "__main__":
    stream_data()  # Start streaming data for 5 vehicles, updating every 2 seconds
