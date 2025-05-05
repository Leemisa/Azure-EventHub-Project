import time 
import json
import random
import uuid
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData


# Azure Event Hub configuration
CONNECTION_STR = 'Endpoint=sb://itri613-eventhub-project.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=rKS5pwvUrH+YE023CbZtxgcWp/xuyB0tz+AEhNwNLQM=;EntityPath=itri613-eventhub-hub'
EVENTHUB_NAME = 'itri613-eventhub-hub'  
# Create Event Hub producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Function to generate stock data
def generate_stock_data():
    symbols_info = {
        "AAPL": {"company_name": "Apple Inc.", "industry": "Technology", "market_cap": "2.5T"},
        "GOOGL": {"company_name": "Alphabet Inc.", "industry": "Technology", "market_cap": "1.8T"},
        "MSFT": {"company_name": "Microsoft Corp.", "industry": "Technology", "market_cap": "2.4T"},
        "AMZN": {"company_name": "Amazon.com Inc.", "industry": "E-Commerce", "market_cap": "1.6T"},
        "TSLA": {"company_name": "Tesla Inc.", "industry": "Automotive", "market_cap": "800B"}
    }

    symbol = random.choice(list(symbols_info.keys()))
    info = symbols_info[symbol]

    price = round(random.uniform(100, 500), 2)
    change_percent = round(random.uniform(-5, 5), 2)
    open_price = round(price * (1 - change_percent / 100), 2)
    volume = random.randint(100, 5000)
    market_status = random.choice(["Open", "Closed"])
    timestamp = datetime.utcnow().isoformat()

    # Compose the payload
    data = {
        "id": f"{symbol}_{timestamp}",  # Cosmos DB requires an 'id' field
        "symbol": symbol,
        "company_name": info["company_name"],
        "industry": info["industry"],
        "market_cap": info["market_cap"],
        "price": price,
        "open_price": open_price,
        "change_percent": change_percent,
        "volume": volume,
        "market_status": market_status,
        "timestamp": timestamp,
        "partitionKey": f"{symbol}_{info['industry']}_{market_status}"  # Partition Key field
    }

    return data

# Main loop to stream stock data
def stream_stock_data():
    print("Starting stock data stream to Azure Event Hub...")
    try:
        with producer:
            while True:
                data = generate_stock_data()
                event_batch = producer.create_batch()
                event_batch.add(EventData(json.dumps(data)))
                producer.send_batch(event_batch)
                print(f"Sent: {data}")
                time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    stream_stock_data()
