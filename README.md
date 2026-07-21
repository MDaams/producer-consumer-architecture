# Queue Architecture POC

A proof of concept implementation for queue-based architecture using producer and consumer patterns.

## Project Structure

- `producer.py` - Producer implementation for the queue system
- `consumer.py` - Consumer implementation for the queue system
- `models/` - Data models for the queue system
  - `entrance_tickets.py` - Ticket-related models

## Getting Started

### Installation

Install dependencies using Poetry:

```bash
poetry install
```

### Setup

This project uses **CloudAMQP** as the message broker. Set up your CloudAMQP queue and add the connection URL to a `.env` file:

```
AMQP_URL=amqps://username:password@your-cloudamqp-url
```

See `env.example` for reference.

### Usage

Run the producer and consumer as needed for your queue architecture testing:

```bash
# Start the producer (fire and forget - sends 100 messages then exits)
poetry run python producer.py

# Start the consumer (runs until stopped - Ctrl+C to exit)
poetry run python consumer.py
```

**Producer**: Fire-and-forget implementation that sends 100 ticket scan messages to the queue and then exits.

**Consumer**: Long-running service that continuously processes messages from the RabbitMQ broker. Stop it by pressing Ctrl+C.

## Requirements

See `pyproject.toml` for project dependencies.
