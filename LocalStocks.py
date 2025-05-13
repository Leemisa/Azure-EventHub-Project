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

# Local company info (South African)
symbols_info = {
    "SOL": {
        "company_name": "Sasol Limited",
        "industry": "Energy",
        "sector": "Oil & Gas",
        "listing_board": "JSE Top 40",
        "currency": "ZAR",
        "isin": "ZAE000006896"
    },
    "NPN": {
        "company_name": "Naspers Limited",
        "industry": "Media",
        "sector": "Consumer Services",
        "listing_board": "JSE Main Board",
        "currency": "ZAR",
        "isin": "ZAE000015889"
    },
    "AGL": {
        "company_name": "Anglo American plc",
        "industry": "Mining",
        "sector": "Metals & Minerals",
        "listing_board": "JSE Top 40",
        "currency": "ZAR",
        "isin": "GB00B1XZS820"
    },
    "MTN": {
        "company_name": "MTN Group Limited",
        "industry": "Telecommunications",
        "sector": "Telecom Services",
        "listing_board": "JSE Main Board",
        "currency": "ZAR",
        "isin": "ZAE000042164"
    },
    "SBK": {
        "company_name": "Standard Bank Group",
        "industry": "Banking",
        "sector": "Financials",
        "listing_board": "JSE Main Board",
        "currency": "ZAR",
        "isin": "ZAE000109815"
    }
}

# Function to generate and publish local stock events
def stream_local_stock():
    print("Starting local stock data stream...")
    try:
        with producer:
            while True:
                symbol = random.choice(list(symbols_info.keys()))
                info = symbols_info[symbol]

                price = round(random.uniform(100, 5000), 2)
                change_percent = round(random.uniform(-5, 5), 2)
                open_price = round(price * (1 - change_percent / 100), 2)
                volume = random.randint(500, 20000)
                market_status = random.choice(["Open", "Closed"])

                # Read timestamp from the shared file
                with open('shared_timestamp.txt', 'r') as f:
                    timestamp = f.read().strip()

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
                print(f"[LOCAL]  Sent: {data}")

                time.sleep(2)
    except KeyboardInterrupt:
        print("Local stream stopped by user.")

if __name__ == '__main__':
    stream_local_stock()