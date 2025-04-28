# 🚚 Real-Time Transportation Data Generator

This Python script simulates real-time transportation data from moving vehicles such as taxis, buses, or delivery vans. It is designed to mimic a real-world streaming scenario where data is continuously generated and can be ingested into a stream processing pipeline (in this case Azure Event Hubs).

## 📜 Description

The script uses the `Faker` library to generate realistic-looking, synthetic transportation data including:
- **Vehicle ID**
- **Latitude & Longitude (GPS location)**
- **Speed (km/h)**
- **Passenger count**
- **Trip ID**
- **Timestamp**

Data is generated at a regular interval (e.g., every 1 second) and printed to the console. This can be easily redirected or integrated with stream services like Azure Event Hubs.

## 🧰 Tools Used

- **Python 3.x**
- **Faker** — to generate fake but realistic data
- **Random & Time** — for variability and real-time simulation
- **JSON** — to structure the data

## 🧪 Installation

Make sure Python is installed. Then, install required packages:

```bash
pip install faker
