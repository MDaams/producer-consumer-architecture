import pika
import json
import time

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
AMQP_URL = os.getenv('AMQP_URL')

# Initialize connection parameters from AMQP URL
# This allows flexible configuration across different environments
params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the message queue with durability enabled to ensure messages survive broker restarts
channel.queue_declare(queue='ticket_scans', durable=True)

print("🚀 Starting producer. Sending data to queue...")

# Simulate 100 ticket scan events. Send raw JSON payloads without Pydantic models
# This reflects real-world scenarios where the producer and consumer may have
# different data models or the producer lacks access to shared model definitions
for i in range(100):
    payload = {
        "ticket_id": f"TICKET-{i}",
        "gate_id": f"GATE-{i % 5}",
        "ruis": "Pizza, friet, cola",
        "timestamp": time.time()
    }
    
    channel.basic_publish(
        exchange='',
        routing_key='ticket_scans',
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Enable message persistence (delivery_mode=2)
    )

print("✅ Successfully sent 100 messages to queue.")
connection.close()