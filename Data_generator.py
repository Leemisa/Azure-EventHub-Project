import time
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Event Hub Configurations
CONNECTION_STR = 'Endpoint=sb://itri613-eventhub-project.servicebus.windows.net/;SharedAccessKeyName=ITRI613-EVENTHUB-PROJECT-StreamAnalytics_it_policy;SharedAccessKey=fmqa6FH0SRpDeYc7KLAuddGQKEWyUmFYj+AEhIKuHys=;EntityPath=itri613-eventhub-hub'
EVENTHUB_NAME = 'itri613-eventhub-hub'  

# Create a producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Function to generate dummy stock data
def generate_stock_data():
    symbols_info = {
        "AAPL": {"company_name": "Apple Inc.", "industry": "Technology", "market_cap": "2.5T"},
        "GOOGL": {"company_name": "Alphabet Inc.", "industry": "Technology", "market_cap": "1.8T"},
        "MSFT": {"company_name": "Microsoft Corp.", "industry": "Technology", "market_cap": "2.4T"},
        "AMZN": {"company_name": "Amazon.com Inc.", "industry": "E-Commerce", "market_cap": "1.6T"},
        "TSLA": {"company_name": "Tesla Inc.", "industry": "Automotive", "market_cap": "800B"}
    }
    
    symbol = random.choice(list(symbols_info.keys()))
    company_info = symbols_info[symbol]
    
    price = round(random.uniform(100, 500), 2)
    volume = random.randint(100, 5000)
    change_percent = round(random.uniform(-5, 5), 2)  # random % change
    open_price = round(price * (1 - (change_percent / 100)), 2)  # simulate opening price
    market_status = random.choice(["Open", "Closed"])
    
    data = {
        "symbol": symbol,
        "company_name": company_info["company_name"],
        "industry": company_info["industry"],
        "market_cap": company_info["market_cap"],
        "price": price,
        "open_price": open_price,
        "change_percent": change_percent,
        "volume": volume,
        "market_status": market_status,
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
