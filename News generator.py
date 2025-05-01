import time
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Configuration for second Event Hub
CONNECTION_STR = 'Endpoint=sb://itri613-eventhub-project.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=rKS5pwvUrH+YE023CbZtxgcWp/xuyB0tz+AEhNwNLQM=;EntityPath=itri613-eventhub-hub'
EVENTHUB_NAME = 'itri613-eventhub-hub'  
# Create producer
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# Function to generate dummy news sentiment
def generate_news_data():
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    sentiments = ["positive", "neutral", "negative"]
    headlines = [
        "hits all-time high in stock value",
        "announces major product launch",
        "under investigation for anti-trust issues",
        "reports unexpected quarterly losses",
        "partners with AI startup"
    ]

    symbol = random.choice(symbols)
    sentiment = random.choice(sentiments)
    headline = f"{symbol} {random.choice(headlines)}"

    data = {
        "symbol": symbol,
        "sentiment": sentiment,
        "headline": headline,
        "timestamp": datetime.utcnow().isoformat()
    }
    return data

# Main loop to send news sentiment data
def stream_news_data():
    print("Starting news sentiment stream...")
    try:
        while True:
            data = generate_news_data()
            event_data = EventData(json.dumps(data))
            with producer:
                event_batch = producer.create_batch()
                event_batch.add(event_data)
                producer.send_batch(event_batch)
            print(f"Sent: {data}")
            time.sleep(3)  # every 3 seconds
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    stream_news_data()
