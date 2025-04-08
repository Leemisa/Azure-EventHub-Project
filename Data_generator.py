import json  # To format our data as JSON
import time  # To add delay (simulate streaming)
import random  # To generate random values for location, speed, etc.
from faker import Faker  # To create fake/realistic-looking data
from datetime import datetime  # To get current time in ISO format
from azure.eventhub import EventHubProducerClient, EventData  # Azure Event Hub SDK

# ──────────────────────────────────────────────
# Azure Event Hub Configuration – update with your actual values
# ──────────────────────────────────────────────
CONNECTION_STR = 'Endpoint=sb://<YOUR_NAMESPACE>.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<YOUR_KEY>'
EVENTHUB_NAME = '<YOUR_EVENT_HUB_NAME>'

# Create a Faker instance to generate dummy data
fake = Faker()

# Initialize the Azure Event Hub Producer Client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Function to generate a single data point for a given vehicle
def generate_data(vehicle_id):
    return {
        "vehicle_id": vehicle_id,  # Unique ID of the taxi/vehicle
        "latitude": round(random.uniform(-34.0, -22.0), 6),  # Latitude within South Africa
        "longitude": round(random.uniform(18.0, 32.0), 6),  # Longitude within South Africa
        "speed_kmh": round(random.uniform(0, 120), 2),  # Speed in km/h between 0 and 120
        "status": random.choice(["en route", "idle", "maintenance"]),  # Random operational status
        "timestamp": datetime.utcnow().isoformat()  # Current UTC time in ISO format
    }

# Function to simulate continuous data streaming and send to Event Hub
def stream_data(num_vehicles=5, interval=2):
    # Generate vehicle IDs like Taxi-1, Taxi-2, etc.
    vehicle_ids = [f"Taxi-{i+1}" for i in range(num_vehicles)]

    try:
        # Loop indefinitely to simulate continuous data streaming
        while True:
            # Create a new batch of event data to send
            event_data_batch = producer.create_batch()

            # Generate and add data for each vehicle to the batch
            for vehicle_id in vehicle_ids:
                data = generate_data(vehicle_id)  # Generate dummy vehicle data
                json_data = json.dumps(data)  # Convert Python dict to JSON string
                print(json_data)  # Print to console (for debugging/logging)
                event_data_batch.add(EventData(json_data))  # Add data to the batch

            # Send the entire batch to Azure Event Hub
            producer.send_batch(event_data_batch)

            # Wait before sending the next batch (simulate real-time data)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Streaming stopped by user.")

    finally:
        # Always close the producer to release resources
        producer.close()

# Entry point of the script
if __name__ == "__main__":
    stream_data()  # Start streaming data for 5 vehicles, updating every 2 seconds
