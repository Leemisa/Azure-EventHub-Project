
# 📈 Real-Time Stock Data Streamer to Azure Event Hub

---

## Overview
This project implements a **Python-based real-time data streaming client** that generates simulated stock market data and sends it continuously to an **Azure Event Hub**.  
It is designed to simulate realistic stock trading environments for academic, testing, and stream analytics purposes, serving as an input for real-time processing pipelines on Azure.

---

## Features
- **Dynamic Data Generation**: Randomly generates stock event data with the following attributes:
  - **Stock Symbol**: Selected from a predefined list (`AAPL`, `GOOGL`, `MSFT`, `AMZN`, `TSLA`).
  - **Price**: A floating-point number between $100 and $500.
  - **Volume**: A random integer between 100 and 5000 shares.
  - **Timestamp**: Current UTC time in ISO 8601 format.
- **Event Streaming**: Continuously sends generated data to Azure Event Hub at two-second intervals.
- **Scalable Architecture**: Easily extendable for additional symbols, data points, or faster/slower intervals.
- **User-Friendly Shutdown**: Allows graceful exit via keyboard interruption (`CTRL+C`).

---

## Requirements
- Python 3.7 or newer
- Azure Event Hub service setup
- Python Package:
  ```bash
  pip install azure-eventhub
  ```

---

## Configuration
The script uses the following configuration:

```python
CONNECTION_STR = ''
EVENTHUB_NAME = ''
```

These settings ensure that events are properly directed to the configured Event Hub namespace and event hub instance.

---

## How It Works
1. Establish a secure connection to the Azure Event Hub using the provided connection string and event hub name.
2. Generate random stock data simulating real-world trading events.
3. Create an event batch and push the generated data into Event Hub at regular two-second intervals.
4. The script keeps streaming data indefinitely until manually stopped.

---

## How to Run the Script
1. Clone or download the Python script to your local environment.
2. Install the required Python package:
   ```bash
   pip install azure-eventhub
   ```
3. Execute the script:
   ```bash
   python stock_streamer.py
   ```
4. Observe real-time events being printed to the console and sent to Azure Event Hub.

---

## Example of a Generated Event
```json
{
  "symbol": "AAPL",
  "price": 267.34,
  "volume": 4230,
  "timestamp": "2025-04-28T20:45:15.123456"
}
```

Console output during execution:
```plaintext
Starting stock data stream to Event Hub...
Sent: {'symbol': 'AAPL', 'price': 267.34, 'volume': 4230, 'timestamp': '2025-04-28T20:45:15.123456'}
Sent: {'symbol': 'GOOGL', 'price': 412.77, 'volume': 1450, 'timestamp': '2025-04-28T20:45:17.456789'}
...
```

---

## Troubleshooting
- **No data in Event Hub**: Ensure that the connection string and event hub name match exactly, and that the Event Hub is running.
- **No module named 'azure.eventhub'**: Install the missing package using `pip install azure-eventhub`.
- **Script exits immediately**: Check your Azure Event Hub permissions and network connectivity.
- **Data not appearing immediately**: Confirm that the Event Hub partition settings and Stream Analytics job configurations match.

---

## License
This project is intended for academic, learning, and non-commercial use only.

---

# 🚀 Start Streaming Real-Time Stock Data Now!
