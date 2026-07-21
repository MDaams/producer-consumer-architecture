import pika
import json
import time

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
from models.entrance_tickets import EntranceTicket

AMQP_URL = os.getenv('AMQP_URL')

params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='ticket_scans', durable=True)

BATCH_SIZE = 10
batch = []
delivery_tags = []

def process_erp_batch(events):
    print(f"\n📦 [ERP WORKER] Received batch of {len(events)} messages")
    print(f"🔄 Sending batch request to ERP...")
    [print(event) for event in events]
    time.sleep(1) # Simulate network latency and ERP processing time
    print(f"✅ [ERP SUCCESS] Batch processed successfully")

print("🤖 Consumer started, listening on queue...")

while True:
    method_frame, header_frame, body = channel.basic_get(queue='ticket_scans', auto_ack=False)
    
    if method_frame:
        ticket = EntranceTicket.model_validate_json(body)
        batch.append(ticket)
        delivery_tags.append(method_frame.delivery_tag)
        
        if len(batch) >= BATCH_SIZE:
            process_erp_batch(batch)
            
            for tag in delivery_tags:
                channel.basic_ack(delivery_tag=tag)
                
            batch.clear()
            delivery_tags.clear()
    else:
        if batch:
            process_erp_batch(batch)
            for tag in delivery_tags:
                channel.basic_ack(delivery_tag=tag)
            batch.clear()
            delivery_tags.clear()
            
        time.sleep(0.5)