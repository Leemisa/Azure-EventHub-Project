import time
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Azure Event Hub configuration
CONNECTION_STR = (
    'Endpoint=sb://itri613-eventhub-project.servicebus.windows.net/;'
    'SharedAccessKeyName=RootManageSharedAccessKey;'
    'SharedAccessKey=rKS5pwvUrH+YE023CbZtxgcWp/xuyB0tz+AEhNwNLQM=;'
    'EntityPath=itri613-eventhub-hub'
)
EVENTHUB_NAME = 'itri613-eventhub-hub'

# Create Event Hub producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Global company info
symbols_info = {
    "AAPL": {
        "company_name": "Apple Inc.",
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "listing_board": "NASDAQ",
        "currency": "USD",
        "isin": "US0378331005"
    },
    # Add other companies here
}

# Function to generate and publish global stock events
def stream_global_stock():
    print("Starting global stock data stream...")
    try:
        with producer:
            while True:
                symbol = random.choice(list(symbols_info.keys()))
                info = symbols_info[symbol]

                price = round(random.uniform(100, 500), 2)
                change_percent = round(random.uniform(-5, 5), 2)
                open_price = round(price * (1 - change_percent / 100), 2)
                volume = random.randint(100, 5000)
                market_status = random.choice(["Open", "Closed"])
                timestamp = datetime.utcnow().isoformat()

                # Write the shared timestamp for the local script
                with open('shared_timestamp.txt', 'w') as f:
                    f.write(timestamp)

                data = {
                    "id": f"{symbol}_{timestamp}",
                    "symbol": symbol,
                    "company_name": info["company_name"],
                    "industry": info["industry"],
                    "sector": info["sector"],
                    "listing_board": info["listing_board"],
                    "currency": info["currency"],
                    "isin": info["isin"],
                    "price": price,
                    "open_price": open_price,
                    "change_percent": change_percent,
                    "volume": volume,
                    "market_status": market_status,
                    "timestamp": timestamp,
                    "partitionKey": f"{symbol}_{info['industry']}_{market_status}"
                }

                event_batch = producer.create_batch()
                event_batch.add(EventData(json.dumps(data)))
                producer.send_batch(event_batch)
                print(f"[GLOBAL] Sent: {data}")

                time.sleep(2)
    except KeyboardInterrupt:
        print("Global stream stopped by user.")

if __name__ == '__main__':
    stream_global_stock()