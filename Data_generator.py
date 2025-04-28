import time
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Event Hub Configurations
CONNECTION_STR = 'Endpoint=sb://itri613-eventhub-project.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=rKS5pwvUrH+YE023CbZtxgcWp/xuyB0tz+AEhNwNLQM=;EntityPath=itri613-eventhub-hubsource'
EVENTHUB_NAME = 'itri613-eventhub-hubsource'

# Create a producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Function to generate dummy stock data
def generate_stock_data():
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    symbol = random.choice(symbols)
    price = round(random.uniform(100, 500), 2)
    volume = random.randint(100, 5000)
    data = {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": datetime.utcnow().isoformat()
    }
    return data

# Main loop to send data
def stream_stock_data():
    print("Starting stock data stream to Event Hub...")
    try:
        with producer:
            while True:
                data = generate_stock_data()
                event_batch = producer.create_batch()
                event_batch.add(EventData(json.dumps(data)))
                producer.send_batch(event_batch)
                print(f"Sent: {data}")
                time.sleep(2)  # send every 2 seconds
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    stream_stock_data()
